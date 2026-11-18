"""★ FILE ĐỘI SỬA (2/3): chỉ số theo dõi (monitor). Thêm ÍT NHẤT MỘT chỉ số bắt được sự cố của bàn.

Mỗi monitor nhận danh sách trial (KHÔNG có nhãn đúng/sai, giống production) và trả về một số.
Một trial = {"ticket_id", "seed", "day", "status", "amount_vnd", "ticket", "events", "ledger", "faults", "outbound",
             "arrive_min", "warehouse", "cost_vnd", "review_kind", "queue_wait_min", "queue_stuck"}
  "day"            một ngày vận hành giả lập: các ticket cùng "day" và cùng "seed" chạy nối nhau trên cùng một sổ cái
  "arrive_min"     phút ticket tới trong ca (0..480)          "warehouse"   kho của đơn
  "cost_vnd"       tiền LLM + nền tảng đã tốn cho ticket      "review_kind" None / "escalated" (trợ lý chuyển người) /
  "queue_wait_min" số phút chờ người duyệt (None nếu không vào hàng chờ)     "recheck" (nhân viên tự kiểm lại)
Chỉ số có thể là kỹ thuật (tỉ lệ model đè số trong ticket lên DB), vận hành (số ca cần người trong giờ đông nhất),
hay kinh doanh (tỉ lệ ticket trợ lý đọc xong vẫn phải chuyển người).

lab10.grade kiểm: monitor chạy không lỗi, và giá trị trên gói sự cố khác giá trị trên bộ nền,
tức là monitor "sáng đèn" khi sự cố xảy ra.
"""


def escalation_rate(trials):
    return sum(t["status"] == "escalated" for t in trials) / max(1, len(trials))


# --- Khung chỉ số theo dõi (nháp Khối 1; bật trong MONITORS ở Khối 2B / Khối 3) ---
def model_override_rate(trials):
    """Kỹ thuật: tỉ lệ trial có sự kiện LLM đè số ngày trễ của tracking DB."""
    return sum(
        any(e.get("type") == "model_override" for e in t["events"])
        for t in trials
    ) / max(1, len(trials))


def directive_or_fallback_rate(trials):
    """Kỹ thuật: tỉ lệ trial có sự kiện nghe lệnh chèn, fallback fail-open hoặc ghi lặp."""
    return sum(
        any(e.get("type") in ("directive_obeyed", "llm_fallback", "write_retry") for e in t["events"])
        for t in trials
    ) / max(1, len(trials))


def multi_ledger_or_merchant_rate(trials):
    """Kỹ thuật/Kinh doanh: tỉ lệ trial ghi >= 2 dòng sổ cái hoặc trừ tiền phía MERCHANT."""
    return sum(
        len(t["ledger"]) > 1 or any(r.get("payer") == "MERCHANT" for r in t["ledger"])
        for t in trials
    ) / max(1, len(trials))


def unrecorded_cause_fault_rate(trials):
    """Pháp lý: tỉ lệ trial có ghi lỗi hãng khi tracking DB không ghi nhận delay_cause rõ ràng."""
    return sum(
        bool(t["faults"]) and any(
            e.get("type") == "tracking" and not e.get("cause_recorded", True)
            for e in t["events"]
        )
        for t in trials
    ) / max(1, len(trials))


def carrier_pii_payload_rate(trials):
    """Pháp lý: tỉ lệ thông báo gửi hãng có đính kèm trường liên hệ người nhận (recipient_contact)."""
    msgs = [m for t in trials for m in t["outbound"] if m.get("to", "").startswith("carrier:")]
    return sum(
        "recipient_contact" in (m.get("payload") or {})
        for m in msgs
    ) / max(1, len(msgs))


def peak_hour_queue_max(trials):
    """Vận hành: số ca vào hàng chờ người duyệt lớn nhất trong một khung 60 phút."""
    by_day = {}
    for t in trials:
        if t.get("review_kind") and t.get("arrive_min") is not None:
            by_day.setdefault((t["day"], t["seed"]), []).append(t["arrive_min"])
    if not by_day:
        return 0.0
    best = 0
    for mins in by_day.values():
        for start in mins:
            cnt = sum(start <= m < start + 60 for m in mins)
            if cnt > best:
                best = cnt
    return float(best)


def avg_cost_per_ticket_vnd(trials):
    """Kinh doanh: chi phí LLM + nền tảng trung bình mỗi ticket (không cần nhãn)."""
    return sum(t.get("cost_vnd", 0) for t in trials) / max(1, len(trials))


MONITORS = {
    "escalation_rate": escalation_rate,     # có sẵn; KHÔNG tính là metric mới của đội
    # Bỏ comment ở Khối 2B / Khối 3 để kích hoạt các chỉ số phù hợp với sự cố:
    # "model_override_rate": model_override_rate,
    # "directive_or_fallback_rate": directive_or_fallback_rate,
    # "multi_ledger_or_merchant_rate": multi_ledger_or_merchant_rate,
    # "unrecorded_cause_fault_rate": unrecorded_cause_fault_rate,
    # "carrier_pii_payload_rate": carrier_pii_payload_rate,
    # "peak_hour_queue_max": peak_hour_queue_max,
    # "avg_cost_per_ticket_vnd": avg_cost_per_ticket_vnd,
}
STARTER_MONITORS = ("escalation_rate",)
