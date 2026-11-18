# Team

## Thông tin nhóm

- Tên nhóm (`TenNhom`, không dấu, không khoảng trắng): `ComVoHan`
- Lớp: `L3A`
- Repo của bàn: `K5-L3A-DAY10-ComVoHan-PoCtoPilotGate1`
- Thẻ sự cố đã bốc (S1–S8): *(điền ngay sau phút 125, khớp dòng `Thẻ đã bốc:` ở đầu `templates/form-c-incident.md`)*

## Thành viên

Họ tên đầy đủ và MSSV của **mọi** thành viên; thêm dòng nếu cần. Vai: Kỹ sư cổng · Sản phẩm và kinh doanh · Vận hành và pháp lý (README mục 3, phút 0–15).

| STT | Họ và tên | MSSV | Vai | Trưởng nhóm |
| --: | --------- | ---- | --- | :---------: |
|   1 | `<Ho va ten TV1>` | `2A202603475` | Kỹ sư cổng (Cổng & Lệnh hệ thống) | X |
|   2 | `<Ho va ten TV2>` | `<MSSV2>` | Kỹ sư cổng (Đo lường, Test & Giám sát) | |
|   3 | `<Ho va ten TV3>` | `<MSSV3>` | Sản phẩm và kinh doanh | |
|   4 | `<Ho va ten TV4>` | `<MSSV4>` | Vận hành và pháp lý | |

Ghi `members` trong `submission/submission.json` theo dạng `"HoVaTen-MSSV"`, khớp bảng trên (ví dụ `["NguyenVanAn-20241234", ...]`).

## Bảng phối hợp nhanh theo khung giờ (240 phút)

> Phân công tối ưu cho nhóm 4 người (2 Kỹ sư cổng · 1 Sản phẩm và kinh doanh · 1 Vận hành và pháp lý) để song song hoá các khối 20–25 phút mà không dồn việc vào một người. Nếu nhóm chỉ có 1 người chuyên code, chuyển `1.5`, `2.7`, `C4`, `C6/C9` sang TV3/TV4 và giữ TV1 làm Kỹ sư cổng duy nhất.

| Khung giờ | TV1 · Kỹ sư cổng (Trưởng nhóm) | TV2 · Kỹ sư cổng (Đo lường & Monitor) | TV3 · Sản phẩm & Kinh doanh | TV4 · Vận hành & Pháp lý |
|---|---|---|---|---|
| **0–15'** (CP1) | Gắn `upstream`, đặt Git local `<MSSV>` / `<MSSV>@example.com`, mời team chấm, chạy `unittest` | Chạy `unittest`, đọc cấu trúc `guards.py`/`monitors.py`/`world.json` | Chọn 1 Eval card + 1 PRD v1.1 từ Lab 9 làm bản chung | Điền khung `TEAM.md`, chuẩn bị `submission/submission.json` |
| **15–60'** (Khối 1 · Phiếu A) | Soát kỹ thuật & tính khả thi của các ngưỡng JSON | **Câu 1.3** (A2 Offline), **1.5** (A3 CI 95%), soát công thức `world.json` cho **1.6** | **Câu 1.1** (A1), **1.6** (A4 & `acceptance_criteria.json`) | **Câu 1.2** (A1 chị Oanh/chị Hạnh), **1.4** (A2 Telemetry prod) |
| **60–65'** (CP2 · Ký) | Chạy `lab10.criteria sign`, commit `'Sign acceptance criteria'`, push `origin main`, điền **A5** | Kiểm tra `criteria verify` & hash khoá | Chốt lần cuối `acceptance_criteria.json` trước khi ký | Kiểm đủ mục Phiếu A trước khi khoá |
| **65–85'** (Khối 2A · Rủi ro) | **Câu 2.1** (B1, B0#1), **Câu 2.2** (B2 `trace T-002@55`), góp nhánh kỹ thuật cho **B4** | Phân tích tự chặn vs người duyệt (B1), hướng xử lý & tín hiệu (**B2**) | **Câu 2.3** (B3 Bản đồ dữ liệu & drift 3 tháng) | **Câu 2.4** (B4 HAZOP vòng 1 + B5 Checklist 9 nhóm có PIC) |
| *(75–85')* **Câu 2.5** | Cả bàn làm Pre-mortem 4 lăng kính (B6): TV1 & TV2 chốt Kỹ thuật · TV3 chốt Kinh doanh & điều phối · TV4 chốt Vận hành & Pháp lý | | | |
| **85–105'** (Khối 2B · Cổng v1) | **Câu 2.6**: code 2–3 cổng trong `lab10/guards.py`, chạy `eval base after` & `unittest`, điền B7.1 & B0#2 | **Câu 2.7** (B7.2 chống rò rỉ), **Câu 2.8** (B7.3 behavioral test `--adhoc`), rà regression | **Câu 2.9** (B7.4 + `operating_gates.json` mục `business`), đồng ra đề `--adhoc` (**2.8**) | **Câu 2.10** (B7.5 Runbook 1–3, B7.6 Giờ cao điểm + `operating_gates.json` mục `operations`, `legal`) |
| **105–115'** (CP3 · v1) | Chạy `lab10.checkpoint`, `eval base prepared`, `gate`, B0#3; commit & push chốt vòng 1 | Kiểm tra không lỗi mới ở `prepared` | Chủ trì viết **quyết định v1** (B8) cùng cả bàn chốt | Rà khớp số config với Runbook 1–3 & PIC ký B8 |
| **125–135'** (CP4 · Nhận thẻ) | `git pull ... upstream main`, bốc thẻ, chạy ngay `lab10.grade --incident Sx` (B1/C0#1) | Ghi nhận bảng 3 mốc đầu tiên ở `prepared` | Mở lại pre-mortem **C1** (lăng kính Kinh doanh) | Ghi `Thẻ đã bốc: Sx` vào đầu Phiếu C & `TEAM.md`; điền **C1** |
| **135–155'** (Phân tích) | Trace ≥ 2 ticket hỏng (`C2`), điền lỗi & nguồn | Hoàn thiện **C2** (tác hại, hướng xử lý), vẽ **C6** (Fault tree trước sửa) | **C4** (HAZOP thẻ), **Câu 3.2** (C5 Spec), bổ sung nhánh **C6** | **C3** (Phần riêng theo thẻ), **Câu 3.3** (C5 Giả định môi trường), bổ sung **C6** |
| **155–185'** (Sửa & Monitor) | **Câu 3.5**: sửa `lab10/guards.py`, chạy `eval Sx after`, `eval base after`, `grade` (`C0` #2–4) | **Câu 3.6**: viết metric mới trong `lab10/monitors.py` (`C8`), tổng hợp **C7**, vẽ **C9** (Fault tree sau sửa) | Chỉnh `operating_gates.json` (`business`), viết **C10** (Risk register) | Chỉnh `operating_gates.json` (`operations`, `legal`), viết **C11** (Checklist + Runbook 4–5) |
| **185–200'** (CP5 · v2) | Kiểm tra `code_hash` & `regression` sạch | Kiểm tra `monitor ✅` & 2 ticket hiểm cho demo | Chủ trì viết **C12** (Quyết định `v2`, mục "Chỉ ở v2", **3 dòng bắt buộc**) | Điền `submission/submission.json`, chạy `check_submission --collect` tới `ĐỦ THÀNH PHẦN` |
| **200–240'** (Demo & Nộp) | Demo 3 mốc & phần sửa cổng; sau demo khôi phục số `v2`, chạy lại `grade` + `--collect`, push cuối | Demo `--adhoc` & chỉ số `monitors.py`; hỗ trợ phản biện bàn bạn | Demo logic kinh doanh/ROI & quyết định `v2` | Demo quy trình/runbook/pháp lý; **cả 4 người** hoàn thành `TEAM.md` & tự nộp link LMS |

---

## Cá nhân

Mỗi thành viên tự đổi tiêu đề `## HoVaTenX-MSSVX` bên dưới thành họ tên không dấu và MSSV của mình (ví dụ `## NguyenVanAn-20241234`), đồng thời điền phần đóng góp, bằng chứng và exit ticket trước khi nộp.

---

## HoVaTen1-2A202603475

### Phần việc phụ trách

- **Vai trong bàn:** Kỹ sư cổng (Cổng & Lệnh hệ thống) · **Trưởng nhóm**
- **Thiết lập & Git (Phút 0–15, 60–65, 105–115, 125, 230–240):**
  - Tạo/cấu hình repo đúng tên `K5-L3A-DAY10-ComVoHan-PoCtoPilotGate1`, mời tài khoản team chấm quyền Read.
  - Gắn remote `upstream`, cấu hình Git local (`user.name` = MSSV trưởng nhóm, `user.email` = `<MSSV>@example.com`).
  - Thực hiện toàn bộ lệnh đẩy các mốc: ký tiêu chí (`Sign acceptance criteria`), chốt vòng 1 (`v1`), kéo thẻ sự cố (`git pull ... upstream main`), và push bài nộp cuối (`LAB 10: bài nộp`).
- **Câu của đề & Mục phiếu:**
  - Phiếu A: **A5** (chạy lệnh 1 `python -m lab10.criteria sign`, ghi giờ ký & mã commit).
  - Phiếu B: **B0** (dòng 1–3), **Câu 2.1** (**B1** — chạy `eval --suite base --stage base` & `gate`), **Câu 2.2** (**B2** — `trace T-002@55`, điền phần ghi lỗi & tìm nguồn), hỗ trợ nhánh kỹ thuật **B4**/**B5**/**B6**, **Câu 2.6** (**B7.1** — code 2–3 cổng trong `lab10/guards.py` & kiểm `unittest`), chạy `checkpoint` + `eval prepared` + `gate` cho **B8**.
  - Phiếu C: **C0** (dòng 1–4), **Câu 3.0** (chạy `grade --incident Sx` ngay khi nhận thẻ), **Câu 3.1** (**C2** — dò trace ≥ 2 ticket hỏng của thẻ), **Câu 3.5** (sửa `lab10/guards.py`, chạy `eval Sx after`, `eval base after`, `grade --incident Sx`).
  - Demo & hậu demo: trình diễn 3 cột `base · prepared · after`; trả mọi config về bản `v2` sau demo, chạy lại lệnh 6 & lệnh 7 trước khi push cuối.
- **File chính:** `lab10/guards.py`, `TEAM.md` (bảng chung), `templates/form-b-evaluation-gates.md` (`B0`, `B1`, `B2`, `B7.1`), `templates/form-c-incident.md` (`C0`, `C2`).

### Đóng góp cụ thể

*(Điền thực tế đã làm, và ghi rõ phần nào có sử dụng trợ lý AI nếu có.)*

### Bằng chứng

*(Điền mã commit, mã lần chạy `runs/<mã>`, dòng trong phiếu.)*

### Exit ticket

*(Một điều học được, một điều còn chưa chắc.)*

---

## HoVaTen2-MSSV2

### Phần việc phụ trách

- **Vai trong bàn:** Kỹ sư cổng (Đo lường, Behavioral Test & Giám sát)
- **Câu của đề & Mục phiếu:**
  - Khối 0: chạy `python -m unittest discover -s tests -v`, đọc `lab10/helpers.py`, `lab10/ops.py`, `data/world.json`.
  - Phiếu A: **Câu 1.3** (**A2** cột Offline — thiết kế 1 offline metric cho 1 bước của agent), **Câu 1.5** (**A3** — phân tích khoảng tin cậy 95%), soát công thức số liệu `ops_facts`/`ops_limits` và định dạng JSON của `config/acceptance_criteria.json` cho **Câu 1.6**.
  - Phiếu B: hoàn thiện phần phân tích tự chặn vs người duyệt ở **B1**; viết hướng xử lý & tín hiệu theo dõi ở **B2**; tham gia Pre-mortem **B6** (lăng kính Kỹ thuật); rà soát regression/edge case cho `lab10/guards.py`; **Câu 2.7** (**B7.2** — 2 bước tránh rò rỉ dữ liệu); **Câu 2.8** (**B7.3** — 1 tính chất behavioral test + chạy 2 ticket hiểm `--adhoc` lưu cho demo).
  - Phiếu C: hoàn thiện **C2** (tác hại của thẻ, hướng xử lý), **Câu 3.4** (**C6** — vẽ Fault tree TRƯỚC khi sửa: ≥ 2 nhánh ở ≥ 2 tầng khác nhau có bằng chứng), tổng hợp bảng **C7**, **Câu 3.6** (**C8** & `lab10/monitors.py` — viết ≥ 1 hàm monitor mới đăng ký vào `MONITORS`, điền bảng 3 ô + ngưỡng báo động + điểm mù + giá trị base/thẻ), **Câu 3.7** (**C9** — cập nhật Fault tree SAU khi sửa).
  - Demo: trình diễn chạy trực tiếp ticket hiểm `--adhoc` và giá trị `monitors.py` khi phản biện.
- **File chính:** `lab10/monitors.py`, `lab10/guards.py` (phối hợp kiểm thử), `templates/form-a-criteria.md` (`A2` Offline, `A3`), `templates/form-b-evaluation-gates.md` (`B2`, `B7.2`, `B7.3`), `templates/form-c-incident.md` (`C2`, `C6`, `C7`, `C8`, `C9`).

### Đóng góp cụ thể

*(Điền thực tế đã làm, và ghi rõ phần nào có sử dụng trợ lý AI nếu có.)*

### Bằng chứng

*(Điền mã commit, mã lần chạy `runs/<mã>`, dòng trong phiếu.)*

### Exit ticket

*(Một điều học được, một điều còn chưa chắc.)*

---

## HoVaTen3-MSSV3

### Phần việc phụ trách

- **Vai trong bàn:** Sản phẩm và kinh doanh
- **Câu của đề & Mục phiếu:**
  - Khối 0: chọn 1 Eval card và 1 PRD v1.1 từ Lab 9 làm tài liệu chuẩn chung của bàn.
  - Phiếu A: **Câu 1.1** (**A1** — mục tiêu cấp hệ thống theo PRD v1.1 §3), **Câu 1.6** (**A4** — câu tiêu chí "Nếu … thì …", 2 ranh giới đầu ra, soát 4 câu hỏi Bước 2, chốt `business_ops` & ngày xem lại) và điền `config/acceptance_criteria.json` (tên `team` = `K5-L3A-DAY10-ComVoHan-PoCtoPilotGate1`, `signed_by`, `required`, `nice_to_have`, `business_ops`, `stop_condition`, `decision_rule`).
  - Phiếu B: **Câu 2.3** (**B3** — Bản đồ dữ liệu 9 dòng + tóm tắt + ví dụ drift 3 tháng tới), điều phối Pre-mortem **Câu 2.5** (**B6** — lăng kính Kinh doanh & chốt 2–3 cổng phòng ngừa), phối hợp ra đề 2 ticket hiểm **Câu 2.8** (**B7.3**), **Câu 2.9** (**B7.4** & `config/operating_gates.json` mục `business`: `daily_refund_cap_vnd`, `cost_budget_per_ticket_vnd`, `pilot_scope`, `roi_min`), chủ trì chốt **Quyết định Gate 1 · v1** (**B8**).
  - Phiếu C: mở lại Pre-mortem ở **C1** (lăng kính Kinh doanh), **Câu 3.1** (**C4** — HAZOP của thẻ ≥ 3 dòng), **Câu 3.2** (**C5** — viết 1 specification kiểm được bằng code/report), bổ sung nhánh kinh doanh vào **C6**, **Câu 3.5** (sửa `config/operating_gates.json` mục `business`; phối hợp TV2 nếu thẻ S5 về chi phí theo kho), **Câu 3.7** (**C10** — Risk register ≥ 1 dòng gắn với metric trong `monitors.py`/report), chủ trì viết **Quyết định Gate 1 · v2** (**C12** — cột `v2`, mục "Chỉ ở v2", **3 dòng bắt buộc**).
  - Demo: trình bày phần bài toán kinh doanh, chi phí/ROI, phạm vi pilot và lập luận quyết định `v2`.
- **File chính:** `config/acceptance_criteria.json`, `config/operating_gates.json` (mục `business`), `templates/form-a-criteria.md` (`A1`, `A4`), `templates/form-b-evaluation-gates.md` (`B3`, `B6`, `B7.4`, `B8`), `templates/form-c-incident.md` (`C1`, `C4`, `C5`, `C10`, `C12`).

### Đóng góp cụ thể

*(Điền thực tế đã làm, và ghi rõ phần nào có sử dụng trợ lý AI nếu có.)*

### Bằng chứng

*(Điền mã commit, mã lần chạy `runs/<mã>`, dòng trong phiếu.)*

### Exit ticket

*(Một điều học được, một điều còn chưa chắc.)*

---

## HoVaTen4-MSSV4

### Phần việc phụ trách

- **Vai trong bàn:** Vận hành và pháp lý
- **Câu của đề & Mục phiếu:**
  - Phiếu A: **Câu 1.2** (**A1** — mục tiêu từ chị Oanh `NV-OANH` và chị Hạnh `NV-HANH` dựa vào PRD §2, §6 & `data/world.json`), **Câu 1.4** (**A2** cột Telemetry production — thêm khung thời gian, ngưỡng báo động, điểm mù), kiểm tra đủ các mục Phiếu A trước giờ ký.
  - Phiếu B: **Câu 2.4** (**B4** — HAZOP vòng 1 ≥ 3 dòng + ≥ 2 dòng ngoài kỹ thuật; **B5** — Checklist go-live 9 nhóm việc lần 1 có PIC có tên từng dòng), Pre-mortem **Câu 2.5** (**B6** — lăng kính Con người/Vận hành & Pháp lý), **Câu 2.10** (`config/operating_gates.json` mục `operations` & `legal`; **B7.5** — Runbook phần 1–3 khớp con số config & thời hạn dừng; **B7.6** — Giờ cao điểm).
  - Phiếu C: ghi số thẻ vào dòng `Thẻ đã bốc:` ở đầu `templates/form-c-incident.md` & `TEAM.md` ngay khi bốc thẻ; **Câu 3.0** (**C1** — kiểm tra hàng chờ/vượt trần ở mốc `prepared` & mở lại Pre-mortem), **Câu 3.1** (**C3** — phần riêng theo đúng số thẻ đã bốc, lưu ý S4 miễn `C3` chỉ cần bổ sung `B7.6` + `C1`), **Câu 3.3** (**C5** — 1 giả định môi trường ngầm tin có thể sai), bổ sung nhánh vận hành/con người/pháp lý vào **C6**, **Câu 3.5** (sửa `config/operating_gates.json` mục `operations` & `legal`), **Câu 3.7** (**C11** — cập nhật Checklist 9 nhóm có PIC & viết Runbook phần 4–5).
  - Gom bài nộp (**CP5**): điền `submission/submission.json` (`team`, `members` dạng `"HoVaTen-MSSV"` khớp `TEAM.md`, `incident`, `decision_v1`, `decision_v2`, chép nguyên `three_lines` từ **C12**), chạy `python -m lab10.check_submission --collect` và xử lý mọi dòng `[THIẾU]` tới khi in `ĐỦ THÀNH PHẦN`.
  - Demo: trình bày phần con người trực, niềm tin người duyệt, pháp lý bên thứ ba và runbook.
- **File chính:** `config/operating_gates.json` (mục `operations`, `legal`), `submission/submission.json`, `templates/form-a-criteria.md` (`A1`, `A2` Telemetry), `templates/form-b-evaluation-gates.md` (`B4`, `B5`, `B7.5`, `B7.6`), `templates/form-c-incident.md` (`Thẻ đã bốc`, `C1`, `C3`, `C5`, `C11`).

### Đóng góp cụ thể

*(Điền thực tế đã làm, và ghi rõ phần nào có sử dụng trợ lý AI nếu có.)*

### Bằng chứng

*(Điền mã commit, mã lần chạy `runs/<mã>`, dòng trong phiếu.)*

### Exit ticket

*(Một điều học được, một điều còn chưa chắc.)*
