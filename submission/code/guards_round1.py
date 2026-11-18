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


def _is_valid_approval(appr: dict | None, tid: str, oid: str, cid: str, amount: int,
                       as_of: str, expected_approver: str) -> bool:
    """Kiểm tra bản ghi phê duyệt khớp đúng ticket, đơn, khách, còn hạn, đủ hạn mức và đúng người duyệt."""
    if not appr:
        return False
    if appr.get("ticket_id") != tid or appr.get("order_id") != oid or appr.get("customer_id") != cid:
        return False
    if appr.get("status") != "valid" or appr.get("expires_at", "") < as_of:
        return False
    if int(appr.get("max_vnd") or 0) < amount:
        return False
    return not expected_approver or appr.get("approver_id") == expected_approver


def _gate_issue_refund(ctx, action: dict) -> Verdict:
    """Cổng 1: đối chiếu DB/chính sách, chặn chi sai/chi trùng, kiểm phê duyệt và trần hoàn theo khách."""
    tid, oid = action.get("ticket_id"), action.get("order_id")
    cid = ctx.ticket.get("customer_id")
    amt = int(action.get("amount_vnd") or 0)

    if ctx.tools.ledger_rows(ticket_id=tid):
        ctx.log("duplicate_ticket_refund_blocked", ticket_id=tid)
        return Verdict.deny("chặn ghi trùng khoản hoàn cho cùng ticket (write_retry)")

    order, parcel, policy, db_delay = _truth(ctx, oid)
    if not order or not parcel or not policy:
        return Verdict.escalate("thiếu dữ liệu đơn hàng/kiện hàng/chính sách trong DB")

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
        if not _is_valid_approval(cur, tid, oid, cid, amt, ctx.as_of, expected_approver):
            valid = next(
                (a for a in ctx.tools.lookup_approvals(ticket_id=tid, order_id=oid)
                 if _is_valid_approval(a, tid, oid, cid, amt, ctx.as_of, expected_approver)),
                None,
            )
            if valid:
                ctx.log("approval_replaced", old=appr_id, new=valid["approval_id"])
                return Verdict.modify("thay thế bằng phê duyệt hợp lệ của đúng ticket", approval_id=valid["approval_id"])
            ctx.log("invalid_approval_escalated", approval_id=appr_id)
            return Verdict.escalate("thiếu hoặc phê duyệt không hợp lệ/hết hạn, chuyển người duyệt")
        return Verdict.allow()

    cust_cap = ctx.tools.ops_limits().get("max_auto_refund_per_customer_per_day_vnd")
    if cust_cap is not None:
        cust_all_auto = sum(r["amount_vnd"] for r in ctx.tools.ledger_rows(customer_id=cid) if not r.get("approval_id"))
        cust_today = min(ctx.tools.auto_refund_today_vnd(), cust_all_auto)
        if cust_today + amt > cust_cap:
            ctx.log("customer_daily_auto_cap_escalated", customer_id=cid, today=cust_today, asked=amt, cap=cust_cap)
            return Verdict.escalate("vượt trần hoàn tự động theo khách trong ngày, chuyển người duyệt")

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


def pre_guard(ctx):
    """Ghim chính sách đang hiệu lực theo ngày hệ thống (as_of) thay cho cờ index_active."""
    policy = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
    if policy is not None:
        ctx.log("policy_pinned", policy_id=policy["policy_id"])
        return Verdict.allow(policy_id=policy["policy_id"])
    return Verdict.allow()


def write_gate(ctx, action):
    """Kiểm tra trước mọi lệnh ghi qua hai cổng vòng 1."""
    tool = action.get("tool")
    if tool == "issue_refund":
        return _gate_issue_refund(ctx, action)
    if tool == "file_carrier_fault":
        return _gate_file_carrier_fault(ctx, action)
    if tool == "notify_carrier":
        return _gate_notify_carrier(ctx, action)
    return Verdict.allow()
