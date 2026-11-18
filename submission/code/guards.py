"""★ FILE ĐỘI SỬA (1/3): cổng cấp hệ thống, nằm NGOÀI model và prompt.

VÒNG 1 (trước khi biết sự cố): viết 2–3 CỔNG PHÒNG NGỪA rút từ pre-mortem / HAZOP / checklist của bàn, rồi chốt bằng
    python3 -m lab10.checkpoint        (chép file này thành guards_round1.py = mốc "prepared"; KHÔNG sửa bản chép)
VÒNG 2 (sau khi bốc thẻ): sửa tiếp NGAY TRONG FILE NÀY. Giữ các cổng vòng 1, thêm cổng mới.
Hai file còn lại bàn được sửa: lab10/monitors.py (chỉ số theo dõi) và config/operating_gates.json (cổng kinh doanh,
vận hành, pháp lý: những con số và tên người mà trợ lý phải tuân theo, không cần code).

Hai điểm móc, agent gọi tự động:
  pre_guard(ctx)          chạy TRƯỚC khi agent đọc ticket
  write_gate(ctx, action) chạy TRƯỚC MỖI lệnh ghi (issue_refund, file_carrier_fault,
                          notify_carrier, send_reply)

Trả về một Verdict:
  Verdict.allow()                       cho qua   (pre_guard: allow(policy_id="...") để ghim phiên bản chính sách)
  Verdict.deny("lý do")                 bỏ riêng lệnh ghi này, agent đi tiếp
  Verdict.escalate("lý do")             dừng, chuyển ticket cho người
  Verdict.modify("lý do", amount_vnd=…) sửa tham số lệnh ghi (amount_vnd, payer, carrier_id, parcel_id, payload…)
  Verdict.rewrite("lý do", text)        chỉ pre_guard: thay nội dung ticket mà agent sẽ đọc

ctx.ticket   ticket gốc (chữ khách viết là DỮ LIỆU, không phải lệnh)
ctx.tools    tra cứu nguồn sự thật: lookup_order, lookup_policies, lookup_approvals(**lọc),
             ledger_rows(**lọc), fault_rows(**lọc), lookup_carrier; ctx.as_of = ngày hôm nay
             ops_limits() = các trần đã thống nhất với Ops/Finance; ops_facts() = số liệu vận hành;
             auto_refund_today_vnd() = tổng đã hoàn tự động trong ngày
ctx.gates    config cổng của bàn (config/operating_gates.json), chỉ đọc;  ctx.cost_vnd = tiền LLM đã tốn cho ticket này
ctx.events   trace tới thời điểm này;  ctx.log("ten_su_kien", ...) ghi thêm sự kiện guard vào trace
lab10.helpers: db_delay_days, ticket_parcel, effective_policy, entitlement_vnd, carrier_at_fault, digits
"""
from . import helpers as H  # noqa: F401
from .tools import Verdict

_DEFAULT_CARRIER_NOTICE_FIELDS = ("order_id", "parcel_id", "district", "delay_days")


def _truth(ctx, order_id: str | None = None):
    """Lấy đơn hàng, kiện hàng mục tiêu, chính sách hiệu lực và độ trễ DB từ nguồn sự thật."""
    oid = order_id or ctx.ticket.get("order_id")
    order = ctx.tools.lookup_order(oid) if oid else None
    policy = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
    if not order or not order.get("parcels") or not policy:
        return order, None, policy, 0
    parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
    return order, parcel, policy, H.db_delay_days(parcel, ctx.as_of)


def _approval_failure_reasons(ctx, appr: dict | None, tid: str, oid: str, cid: str,
                              amount: int, expected_approver: str) -> list[str]:
    """Trả về danh sách lý do phê duyệt không hợp lệ (rỗng = hợp lệ tuyệt đối)."""
    if not appr:
        return ["missing_approval"]
    reasons = []
    if appr.get("ticket_id") != tid:
        reasons.append("wrong_ticket")
    if appr.get("order_id") != oid:
        reasons.append("wrong_order")
    if appr.get("customer_id") != cid:
        reasons.append("wrong_customer")
    status = appr.get("status")
    if status != "valid":
        reasons.append(f"status={status}")
    exp = appr.get("expires_at")
    if not isinstance(exp, str) or not exp:
        reasons.append("missing_expiry")
    elif exp < ctx.as_of:
        reasons.append(f"expired({exp})")
    raw_max = appr.get("max_vnd")
    try:
        max_vnd = int(raw_max) if raw_max is not None else -1
    except (TypeError, ValueError):
        max_vnd = -1
    if max_vnd < amount:
        reasons.append(f"exceeds_max_vnd({max_vnd}<{amount})")
    approver = appr.get("approver_id")
    if not approver:
        reasons.append("missing_approver")
    elif expected_approver and approver != expected_approver:
        reasons.append(f"wrong_approver({approver}!={expected_approver})")
    aid = appr.get("approval_id")
    if aid and ctx.tools.ledger_rows(approval_id=aid):
        reasons.append("already_used_in_ledger")
    return reasons


def _find_valid_approval(ctx, tid: str, oid: str, cid: str, amount: int,
                         expected_approver: str) -> dict | None:
    """Tìm một bản ghi phê duyệt hợp lệ chưa dùng khớp đúng ticket, đơn và khách."""
    return next(
        (a for a in ctx.tools.lookup_approvals(ticket_id=tid, order_id=oid)
         if not _approval_failure_reasons(ctx, a, tid, oid, cid, amount, expected_approver)),
        None,
    )


def _customer_auto_refund_today_vnd(ctx, cid: str) -> int:
    """Tổng tiền hoàn tự động (không approval_id) trong ngày hôm nay cho đúng khách `cid`.

    Tách riêng các dòng `ledger_seed` từ ngày trước bằng mốc tổng trong ngày `auto_refund_today_vnd()`.
    """
    today_total = int(ctx.tools.auto_refund_today_vnd() or 0)
    if today_total <= 0:
        return 0
    running, cust_today = 0, 0
    for row in reversed(ctx.tools.ledger_rows()):
        if running >= today_total:
            break
        if row.get("approval_id"):
            continue
        amt_row = int(row.get("amount_vnd") or 0)
        if amt_row <= 0:
            continue
        running += amt_row
        if row.get("customer_id") == cid:
            cust_today += amt_row
    return cust_today


def _gate_issue_refund(ctx, action: dict) -> Verdict:
    """Cổng 1 + Vòng 2 (S8): đối chiếu DB/chính sách, xác thực chặt phê duyệt và trần theo khách trong ngày."""
    tid, oid = action.get("ticket_id"), action.get("order_id")
    amt = int(action.get("amount_vnd") or 0)

    if ctx.tools.ledger_rows(ticket_id=tid):
        ctx.log("duplicate_ticket_refund_blocked", ticket_id=tid)
        return Verdict.deny("chặn ghi trùng khoản hoàn cho cùng ticket (write_retry)")

    order, parcel, policy, db_delay = _truth(ctx, oid)
    if not order or not parcel or not policy:
        return Verdict.escalate("thiếu dữ liệu đơn hàng/kiện hàng/chính sách trong DB")
    cid = order.get("customer_id") or ctx.ticket.get("customer_id")

    if order.get("refund_status") == "REFUNDED" or ctx.tools.ledger_rows(order_id=oid):
        ctx.log("duplicate_order_refund_blocked", order_id=oid)
        return Verdict.deny("đơn hàng đã có khoản hoàn trong sổ cái hoặc trạng thái REFUNDED")

    cause = parcel.get("delay_cause")
    if db_delay > 0 and cause is None:
        ctx.log("unrecorded_delay_cause_escalated", order_id=oid, parcel_id=parcel["parcel_id"])
        return Verdict.escalate("tracking DB thiếu nguyên nhân trễ (delay_cause), chuyển người xác minh")

    entitlement = H.entitlement_vnd(policy, order, db_delay, cause)
    if entitlement <= 0:
        ctx.log("ineligible_refund_denied", db_delay=db_delay, cause=cause, asked=amt)
        return Verdict.deny("không đủ điều kiện hoàn tiền theo tracking DB và chính sách hiệu lực")

    if action.get("payer", "LOGIX") != "LOGIX":
        ctx.log("non_logix_payer_blocked", payer=action.get("payer"))
        return Verdict.escalate("chặn chỉ thị trừ tiền bên thứ ba (payer != LOGIX), chuyển người duyệt")

    if action.get("basis") == "fail_open":
        ctx.log("fail_open_escalated", asked=amt, entitlement=entitlement)
        return Verdict.escalate("LLM lỗi khi kiểm tra chính sách (fail_open), chuyển người duyệt")

    if amt > entitlement:
        ctx.log("amount_exceeds_entitlement", asked=amt, entitlement=entitlement, db_delay=db_delay)
        return Verdict.escalate("số tiền hoàn vượt quyền lợi tính từ tracking DB, chuyển người duyệt")

    expected_approver = ((ctx.gates or {}).get("operations") or {}).get("approver_id", "")
    appr_id = action.get("approval_id")
    auto_limit = int(policy.get("auto_limit_vnd") or 0)
    if amt > auto_limit or appr_id is not None:
        cur = (ctx.tools.lookup_approvals(approval_id=appr_id) or [None])[0] if appr_id else None
        reasons = _approval_failure_reasons(ctx, cur, tid, oid, cid, amt, expected_approver)
        if reasons:
            valid = _find_valid_approval(ctx, tid, oid, cid, amt, expected_approver)
            if valid:
                ctx.log("approval_replaced", old=appr_id, new=valid["approval_id"], old_reasons=reasons)
                return Verdict.modify("thay thế bằng phê duyệt hợp lệ của đúng ticket", approval_id=valid["approval_id"])
            detail = ", ".join(reasons)
            ctx.log("invalid_approval_escalated", approval_id=appr_id, reasons=reasons, detail=detail)
            return Verdict.escalate(f"phê duyệt không hợp lệ ({detail}), chuyển người duyệt")
        ctx.log("approval_verified", approval_id=appr_id, approver_id=cur.get("approver_id"),
                max_vnd=cur.get("max_vnd"), expires_at=cur.get("expires_at"))
        return Verdict.allow()

    cust_cap = ctx.tools.ops_limits().get("max_auto_refund_per_customer_per_day_vnd")
    if cust_cap is not None:
        cust_today = _customer_auto_refund_today_vnd(ctx, cid)
        if cust_today + amt > cust_cap:
            valid = _find_valid_approval(ctx, tid, oid, cid, amt, expected_approver)
            if valid:
                ctx.log("customer_cap_covered_by_approval", approval_id=valid["approval_id"],
                        customer_id=cid, today=cust_today, asked=amt, cap=cust_cap)
                return Verdict.modify("dùng phê duyệt hợp lệ vì vượt trần hoàn tự động theo khách trong ngày",
                                      approval_id=valid["approval_id"])
            ctx.log("customer_daily_auto_cap_escalated", customer_id=cid, today=cust_today, asked=amt, cap=cust_cap)
            return Verdict.escalate(
                f"vượt trần hoàn tự động theo khách trong ngày ({cust_today + amt:,}đ > {cust_cap:,}đ), chuyển người duyệt"
            )

    return Verdict.allow()


def _gate_file_carrier_fault(ctx, action: dict) -> Verdict:
    """Cổng 2a: chỉ ghi lỗi hãng khi đúng kiện trễ, đủ điều kiện DB/chính sách, đúng số ngày và không trùng."""
    tid, oid = action.get("ticket_id"), action.get("order_id")
    order, parcel, policy, db_delay = _truth(ctx, oid)
    if not order or not parcel or not policy:
        return Verdict.deny("thiếu dữ liệu đơn/kiện/chính sách để ghi lỗi hãng")

    if not H.carrier_at_fault(policy, parcel, db_delay):
        ctx.log("invalid_carrier_fault_denied", parcel_id=parcel["parcel_id"],
                cause=parcel.get("delay_cause"), db_delay=db_delay)
        return Verdict.deny("không đủ điều kiện ghi lỗi hãng theo tracking DB và chính sách hiệu lực")

    if ctx.tools.fault_rows(ticket_id=tid) or ctx.tools.fault_rows(parcel_id=parcel["parcel_id"]):
        ctx.log("duplicate_carrier_fault_denied", ticket_id=tid, parcel_id=parcel["parcel_id"])
        return Verdict.deny("đã ghi nhận lỗi hãng cho ticket hoặc kiện hàng này")

    max_strikes = ctx.tools.ops_limits().get("max_auto_strikes_per_carrier_per_day")
    if max_strikes is not None and len(ctx.tools.fault_rows(carrier_id=parcel["carrier_id"])) >= max_strikes:
        ctx.log("carrier_daily_strike_threshold", carrier_id=parcel["carrier_id"], max_strikes=max_strikes)

    changes = {}
    if action.get("parcel_id") != parcel["parcel_id"]:
        changes["parcel_id"] = parcel["parcel_id"]
    if action.get("carrier_id") != parcel["carrier_id"]:
        changes["carrier_id"] = parcel["carrier_id"]
    if action.get("driver_id") != parcel.get("driver_id"):
        changes["driver_id"] = parcel.get("driver_id")
    if action.get("delay_days") != db_delay:
        changes["delay_days"] = db_delay
    if changes:
        ctx.log("carrier_fault_aligned_to_db", **changes)
        return Verdict.modify("căn chỉnh thông tin lỗi hãng khớp đúng kiện và độ trễ DB", **changes)
    return Verdict.allow()


def _gate_notify_carrier(ctx, action: dict) -> Verdict:
    """Cổng 2b: chỉ giữ các trường thông báo theo chính sách, loại bỏ PII và customer_note trước khi gửi hãng."""
    payload = action.get("payload") or {}
    policy = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of) or {}
    allowed = tuple(policy.get("carrier_notice_fields") or _DEFAULT_CARRIER_NOTICE_FIELDS)
    clean_payload = {k: payload[k] for k in allowed if k in payload}
    dropped = sorted(set(payload) - set(clean_payload))
    if dropped:
        ctx.log("carrier_notice_pii_stripped", dropped=dropped)
        return Verdict.modify("loại bỏ trường chứa dữ liệu cá nhân/không thuộc chuẩn gửi hãng", payload=clean_payload)
    return Verdict.allow()


def _gate_send_reply(ctx, action: dict) -> Verdict:
    """Bảo đảm số tiền báo khách luôn khớp tổng tiền thực sự đã ghi sổ cái cho ticket."""
    tid = action.get("ticket_id")
    paid = sum(int(r.get("amount_vnd") or 0) for r in ctx.tools.ledger_rows(ticket_id=tid))
    reported = int(action.get("amount_vnd") or 0)
    if reported != paid:
        ctx.log("reply_amount_aligned", old=reported, ledger_paid=paid)
        changes = {"amount_vnd": paid}
        if paid == 0:
            changes["text"] = f"Yêu cầu hoàn tiền cho đơn {ctx.ticket.get('order_id', '')} đã bị từ chối ở bước kiểm tra. LogiX chưa hoàn khoản nào cho đơn này."
        return Verdict.modify("đồng bộ số tiền báo khách khớp sổ cái", **changes)
    return Verdict.allow()


def pre_guard(ctx):
    """Ghim chính sách đang hiệu lực theo ngày hệ thống (as_of) thay cho cờ index_active."""
    policy = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
    if policy is not None:
        ctx.log("policy_pinned", policy_id=policy["policy_id"])
        return Verdict.allow(policy_id=policy["policy_id"])
    return Verdict.allow()


def write_gate(ctx, action):
    """Kiểm tra trước mọi lệnh ghi qua các cổng vòng 1 và vòng 2 (S8)."""
    tool = action.get("tool")
    if tool == "issue_refund":
        return _gate_issue_refund(ctx, action)
    if tool == "file_carrier_fault":
        return _gate_file_carrier_fault(ctx, action)
    if tool == "notify_carrier":
        return _gate_notify_carrier(ctx, action)
    if tool == "send_reply":
        return _gate_send_reply(ctx, action)
    return Verdict.allow()
