# Team

## Thông tin nhóm

- Tên nhóm (`TenNhom`, không dấu, không khoảng trắng): `ComVoHan`
- Lớp: `L3A`
- Repo của bàn: `K5-L3A-DAY10-ComVoHan-PoCtoPilotGate1`
- Thẻ đã bốc: `S8`

## Thành viên

Họ tên đầy đủ và MSSV của **mọi** thành viên; thêm dòng nếu cần. Vai: Kỹ sư cổng · Sản phẩm và kinh doanh · Vận hành và pháp lý (README mục 3, phút 0–15).

| STT | Họ và tên           | MSSV          | Vai                                                             | Trưởng nhóm |
| --: | ------------------- | ------------- | --------------------------------------------------------------- | :---------: |
|   1 | Lý Thanh Lâm        | `2A202603475` | Kỹ sư cổng (Cổng `guards.py`, CLI & Git)                        |      X      |
|   2 | `Vũ Trí Dũng`       | `2A202603478` | Kỹ sư cổng (Đo lường, `monitors.py` & Fault Tree)               |             |
|   3 | `Nguyễn Thanh Tùng` | `2A202603446` | Sản phẩm và kinh doanh (Tiêu chí, Phiếu A–B & Quyết định)       |             |
|   4 | `Phạm Trung Kiên`   | `2A202603479` | Vận hành và pháp lý (`operating_gates.json`, Phiếu C & Runbook) |             |

Ghi `members` trong `submission/submission.json` theo dạng `"HoVaTen-MSSV"`, khớp bảng trên (ví dụ `["NguyenVanAn-20241234", ...]`).

---

## Quy tắc sở hữu file & đầu mối Git (1 file = 1 người sửa)

> Mục tiêu: **0 xung đột Git**, **0 đứt mạch nhật ký** `runs/`, và **không ai phải ngồi chờ** ở Khối 1.
> Các thành viên gõ nháp phần chữ của mình vào doc/chat chung theo đúng mã mục (`A1`, `B2`, `C6`...) để **Form Keeper** dán vào phiếu chuẩn, còn **TV1** chạy mọi lệnh đo/chốt trên 1 máy duy nhất để `runs/journal.jsonl` và `code_hash` đồng bộ hoàn toàn.

| File / Tác vụ                                                                                                      | Chủ sở hữu duy nhất               | Quy tắc phối hợp & bàn giao                                                                                                                |
| ------------------------------------------------------------------------------------------------------------------ | --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| `lab10/guards.py`                                                                                                  | **TV1**                           | Chỉ TV1 sửa cả Vòng 1 & Vòng 2. Nhận đề xuất nhánh cổng từ TV2/TV3/TV4 sau Pre-mortem & Phân tích thẻ                                      |
| Lệnh CLI (`criteria`, `eval`, `trace`, `gate`, `checkpoint`, `grade`, `--collect`) & Git (`upstream`, push `main`) | **TV1**                           | Chỉ TV1 chạy lệnh ghi vào `runs/` và đẩy lên `origin main` tại 4 mốc chốt                                                                  |
| `lab10/monitors.py`                                                                                                | **TV2**                           | Chỉ TV2 viết hàm monitor mới; gửi hoặc commit vào trước khi TV1 chạy `eval` / `grade`                                                      |
| `config/acceptance_criteria.json` + `templates/form-a-criteria.md`                                                 | **TV3** _(Form Keeper Phiếu A)_   | TV2 gửi `1.3`, `1.5`; TV4 gửi `1.2`, `1.4` cho TV3 gộp trước phút 60. Riêng `A5` do TV1 điền sau khi ký. **Cấm sửa file JSON sau phút 65** |
| `templates/form-b-evaluation-gates.md`                                                                             | **TV3** _(Form Keeper Phiếu B)_   | TV1 gửi số chạy máy (`B0`, `B1`, `B2`, `B7.1`); TV2 gửi `B1`, `B2`, `B7.2`, `B7.3`; TV4 gửi `B4`, `B5`, `B7.5`, `B7.6`                     |
| `config/operating_gates.json` _(cả_ `business`_,_ `operations`_,_ `legal`_)_                                       | **TV4**                           | Chỉ TV4 gõ vào JSON để tránh lỗi cú pháp khi 2 người sửa chung. TV3 chốt 4 con số `business` đưa TV4 nhập                                  |
| `templates/form-c-incident.md` + `submission/submission.json`                                                      | **TV4** _(Form Keeper Phiếu C)_   | TV1 gửi `C0` và log trace `C2`; TV2 gửi `C2`, `C6`–`C9`; TV3 gửi `C4`, `3.2`, `C10`, `C12` + `three_lines`                                 |
| `TEAM.md`                                                                                                          | **Cả 4 người** → **TV1** gộp push | Mỗi thành viên tự hoàn thiện 3 tiểu mục cuối của mình rồi gửi TV1 gộp trước lần push cuối                                                  |

---

## Bảng phối hợp theo khung giờ (chạy cuốn chiếu 240 phút)

> **Lưu ý trên Windows:** dùng `python` nếu máy không có `python3`. **Luật cứng:** tuyệt đối KHÔNG chạy `eval` / `trace` / `grade` trước khi commit & push lệnh ký ở phút 60–65.

| Khung giờ                       | TV1 · Kỹ sư cổng 1 (Trưởng nhóm)                                                                                                                               | TV2 · Kỹ sư cổng 2 (Monitor & Test)                                                                                                                                         | TV3 · Sản phẩm & Kinh doanh                                                                                                                  | TV4 · Vận hành & Pháp lý                                                                                                                                                                  |
| ------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **0–15'** _(CP1)_               | Gắn `upstream`, cấu hình Git local (`<MSSV>` / `<MSSV>@example.com`), mời team chấm quyền Read, chạy `unittest` (13 OK)                                        | Đọc `lab10/helpers.py`, `lab10/ops.py`, `data/world.json`                                                                                                                   | Chọn **1 Eval card + 1 PRD v1.1** từ Lab 9 làm bản chung                                                                                     | Điền họ tên/MSSV 4 người vào `TEAM.md` (gửi TV1), mở xem khung `submission.json`                                                                                                          |
| **15–60'** _(Khối 1 · Phiếu A)_ | _(Cuốn chiếu)_ Đọc sâu `agent.py`, `mock_llm.py`, `tools.py`; **phác thảo sẵn logic cổng vòng 1 cho** `guards.py` & nhánh lỗi cho HAZOP _(chưa chạy_ `eval`_)_ | Làm **Câu 1.3** (`A2` Offline), **Câu 1.5** (`A3` CI 95%), soát công thức `ops_facts`/`ops_limits` cho **1.6**; **nháp trước khung** `monitors.py` **& 2 ticket** `--adhoc` | Làm **Câu 1.1** (`A1`), **Câu 1.6** (`A4` + `config/acceptance_criteria.json`); **gom** `1.2`**–**`1.5` **hoàn thiện Phiếu A** trước phút 60 | Làm **Câu 1.2** (`A1` chị Oanh/Hạnh), **Câu 1.4** (`A2` Telemetry prod); _(cuốn chiếu)_ **dựng trước khung Checklist 9 nhóm (**`B5`**) & khung Runbook 1–3 (**`B7.5`**) từ** `world.json` |
| **60–65'** _(CP2 · Ký)_         | Chạy `python -m lab10.criteria sign` → điền **A5** → `commit -m 'Sign acceptance criteria'` → `push origin main`                                               | Chạy `python -m lab10.criteria verify` xác nhận hash khớp                                                                                                                   | Kiểm lại `acceptance_criteria.json` lần cuối trước khi ký _(từ đây KHÔNG mở/lưu lại file này)_                                               | Kiểm Phiếu A đã đủ `A1`–`A4` trước khi đẩy                                                                                                                                                |
| **65–75'** _(Khối 2A)_          | Chạy `eval --suite base --stage base --note "baseline"`, `gate`, `trace T-002@55`; gửi số cho TV3 vào **B0#1, B1, B2**                                         | Phân tích tự chặn vs người duyệt (**B1**), hướng xử lý & tín hiệu (**B2**), chốt 2 ticket `--adhoc` (**2.8**)                                                               | Làm **Câu 2.3** (**B3** Bản đồ dữ liệu & ví dụ drift 3 tháng)                                                                                | Hoàn thiện **Câu 2.4** (**B4** HAZOP vòng 1 ≥ 3 dòng + ≥ 2 dòng ngoài kỹ thuật; **B5** Checklist 9 nhóm có PIC có tên)                                                                    |
| **75–85'** _(Pre-mortem)_       | **Cả bàn họp làm Câu 2.5 (**`B6`**):** 2' viết im lặng → đọc vòng tròn → phủ đủ 4 lăng kính → TV3 điều phối chốt **2–3 cổng phòng ngừa** dựng ngay             |                                                                                                                                                                             |                                                                                                                                              |                                                                                                                                                                                           |
| **85–105'** _(Khối 2B)_         | **Câu 2.6**: hoàn thiện 2–3 cổng trong `guards.py`, chạy `eval base after`, `unittest`, và 2 lệnh `--adhoc` của TV2; gửi **B7.1, B0#2**                        | Viết **Câu 2.7** (**B7.2** chống rò rỉ), đọc kết quả `--adhoc` điền **B7.3**; **viết sẵn monitor nền** trong `monitors.py`                                                  | Làm **Câu 2.9** (**B7.4** lý do có số từ `world.json`), chuyển **4 con số** `business` cho TV4; gom **B0–B7** vào Phiếu B                    | **Độc quyền điền** `operating_gates.json` (cả `business` + `operations` + `legal`); hoàn thiện **Câu 2.10** (**B7.5** Runbook 1–3, **B7.6** Giờ cao điểm)                                 |
| **105–115'** _(CP3 · v1)_       | Chạy `checkpoint` → `eval --suite base --stage prepared` → `gate`; lấy số **B0#3**; sau khi TV3 điền `B8`, commit & push chốt `v1`                             | Kiểm tra không ca nền nào mới hỏng ở mốc `prepared`                                                                                                                         | Chủ trì điền **B8 Quyết định Gate 1 · v1** (cả bàn chốt) & kiểm đủ Phiếu B                                                                   | Rà khớp 100% con số giữa `operating_gates.json` và Runbook 1–3                                                                                                                            |
| **125–135'** _(CP4 · Thẻ)_      | Chạy `git pull ... upstream main` → bốc 1 thẻ `Sx` → chạy ngay `grade --incident Sx` (`C0#1`) → push `origin main` cho cả nhóm đọc thẻ                         | Đọc `grade-report` mốc `prepared` (cổng vòng 1 đỡ được gì)                                                                                                                  | Mở lại Pre-mortem **C1** (lăng kính Kinh doanh)                                                                                              | Ghi `Thẻ đã bốc: Sx` vào đầu Phiếu C & `TEAM.md`; gom **C0#1, C1** vào Phiếu C                                                                                                            |
| **135–155'** _(Phân tích)_      | Chạy `trace --suite Sx` trên **≥ 2 ticket hỏng khác kiểu** (`--seed 11`), gửi log cho TV2 điền `C2`                                                            | Hoàn thiện **C2** (tác hại, ≥ 2 lỗi khác nguồn, ≥ 1 lỗi chìm); chủ trì vẽ khung **C6 Fault tree TRƯỚC sửa**                                                                 | Làm **C4** (HAZOP thẻ ≥ 3 dòng), **Câu 3.2** (**C5** Spec), bổ sung nhánh kinh doanh vào **C6**                                              | Làm **C3** (phần riêng theo đúng thẻ `Sx`; _miễn nếu thẻ_ `S4`), **Câu 3.3** (**C5** Giả định môi trường), bổ sung nhánh vận hành/pháp lý vào **C6**                                      |
| **155–185'** _(Sửa & Monitor)_  | **Câu 3.5**: sửa `guards.py`, chạy `eval Sx after`, `eval base after`, `grade --incident Sx` (`C0#2–4`)                                                        | **Câu 3.6**: thêm ≥ 1 hàm vào `monitors.py` (`C8`), tổng hợp bảng **C7**, vẽ **C9 Fault tree SAU sửa**                                                                      | Chốt chỉnh sửa `business` (gửi TV4), viết **C10 Risk register**, chuẩn bị khung **C12**                                                      | **Độc quyền sửa** `operating_gates.json` (`business`, `operations`, `legal`); viết **C11** (cập nhật Checklist + Runbook 4–5)                                                             |
| **185–200'** _(CP5 · v2)_       | Chạy `grade --incident Sx` xác nhận `monitor ✅` + `regression ✅`; chạy `check_submission --collect` tới khi `ĐỦ THÀNH PHẦN`                                  | Kiểm tra giá trị `monitors.py` sáng đèn trên thẻ & chuẩn bị 2 ticket `--adhoc` cho demo                                                                                     | Chủ trì chốt **C12 Quyết định v2** + mục "Chỉ ở v2" + **3 dòng bắt buộc** (gửi TV4)                                                          | Gom đủ `C0`–`C12` vào Phiếu C; điền `submission/submission.json` (`members`, `three_lines`...)                                                                                            |
| **200–240'** _(Demo & Nộp)_     | Demo 3 mốc & phần sửa cổng; **hậu demo:** trả mọi số về `v2`, chạy lại `grade` + `--collect`, gộp `TEAM.md` cả 4 bạn, push `"LAB 10: bài nộp"`                 | Demo `--adhoc` & `monitors.py`; hỗ trợ phản biện bàn bạn                                                                                                                    | Demo bài toán chi phí/ROI, phạm vi & quyết định `v2`                                                                                         | Demo runbook, nhân sự trực & pháp lý; **cả 4 bạn tự điền Exit ticket & nộp link repo trên LMS**                                                                                           |

---

## Cá nhân

Mỗi thành viên tự đổi tiêu đề `## HoVaTenX-MSSVX` bên dưới thành họ tên không dấu và MSSV của mình (ví dụ `## NguyenVanAn-20241234`), đồng thời điền phần đóng góp, bằng chứng và exit ticket trước khi nộp.

---

## LyThanhLam-2A202603475

### Phần việc phụ trách

- **Vai trong bàn:** Kỹ sư cổng 1 (Chủ sở hữu `lab10/guards.py`, đầu mối CLI & Git · GitHub: `LysLama`) · **Trưởng nhóm**
- **File độc quyền sửa:** `lab10/guards.py` _(cùng quyền tổng hợp & push_ `TEAM.md` _và các mốc Git lên_ `origin main`_)_.
- **Chi tiết từng chặng:**
  - **Phút 0–15 (CP1):** Mời tài khoản team chấm quyền Read; gắn `upstream`; đặt Git local (`2A202603475` / `2A202603475@example.com`); chạy `python -m unittest discover -s tests -v`.
  - **Phút 15–65 (Khối 1 · CP2):** Đọc trước `lab10/agent.py`, `mock_llm.py`, `tools.py`, `helpers.py` để phác thảo nháp các cổng vòng 1 _(chưa chạy_ `eval`_)_. Phút 60–65: chạy `python -m lab10.criteria sign`, ghi **A5**, commit `'Sign acceptance criteria'` và push `origin main`.
  - **Phút 65–115 (Khối 2 · CP3):** Chạy `eval --suite base --stage base`, `gate`, `trace T-002@55` (`Câu 2.1–2.2`, gửi số cho TV3 vào `B0#1, B1, B2`); tham gia Pre-mortem **B6** (lăng kính Kỹ thuật); viết 2–3 cổng vào `lab10/guards.py` (`Câu 2.6`, chạy `eval base after` & `unittest`, chạy 2 lệnh `--adhoc` của TV2 cho `Câu 2.8`, gửi số `B7.1, B0#2`). Phút 105–115: chạy `checkpoint` → `eval base prepared` → `gate`, ghi `B0#3`, commit & push chốt `v1`.
  - **Phút 125–200 (Khối 3 · CP4–CP5):** Phút 125: `git pull --no-rebase --no-edit --allow-unrelated-histories -X ours upstream main`, bốc thẻ `Sx`, chạy ngay `grade --incident Sx` (`Câu 3.0`, `C0#1`), push lên `origin main` cho cả nhóm đọc thẻ. Chạy `trace --suite Sx` ≥ 2 ticket hỏng khác kiểu gửi TV2 (`C2`); sửa `lab10/guards.py` (`Câu 3.5`); chạy `eval Sx after`, `eval base after`, `grade --incident Sx` (`C0#2–4`); chạy `check_submission --collect` tới khi `ĐỦ THÀNH PHẦN`.
  - **Phút 200–240 (Demo & Nộp):** Demo 3 mốc `base · prepared · after` và phần sửa cổng; sau demo khôi phục config về bản `v2`, chạy lại `grade` + `--collect`, gộp mục cá nhân của 4 thành viên vào `TEAM.md`, commit & push lần cuối `"LAB 10: bài nộp"`, gửi link repo cho team chấm và nộp trên LMS.

### Đóng góp cụ thể

- **Thiết lập & CP1–CP2:** Cấu hình Git (`2A202603475` / `2A202603475@example.com`), gắn `upstream`, kiểm tra `unittest` (13/13 pass); thực hiện ký bản tiêu chí `python -m lab10.criteria sign` → tạo `config/acceptance_criteria.lock`, điền **A5** và đẩy commit `Sign acceptance criteria` trước mọi lần chạy đánh giá.
- **Khối 2A–2B & CP3 (`v1`):** Chạy baseline (`T-002@55`), phân tích trace và điền số liệu **B0#1–3, B7.1**; viết bộ cổng vòng 1 trong `lab10/guards.py` (`pre_guard` ghim `effective_policy`, `_gate_issue_refund` kiểm DB/sổ cái/approval/trần ngày theo khách, `_gate_file_carrier_fault`, `_gate_notify_carrier` loại PII); chạy 2 kịch bản `--adhoc` (`O-1025`, `O-1024`, `O-1026`), chạy `checkpoint` → `eval base prepared` → `gate` và đẩy chốt `v1`.
- **CP4 & Khối 3 (Thẻ `S8`):** Đồng bộ `origin/main` (`2abfbb8`), chạy `lab10.grade --incident S8` mốc ban đầu (`C0#1`) và trace các ca lỗi `S8-01`, `S8-02`, `S8-03`, `S8-04`, `S8-06`, `S8-43`, `S8-44` kèm ca đối chứng `S8-05`; nâng cấp `lab10/guards.py` cho Vòng 2: chuẩn hoá `_approval_failure_reasons` (chặn dùng lặp `ledger_rows(approval_id=...)`, an toàn khi `expires_at` null/rỗng, kiểm `approver_id`, trả lý do cụ thể ra trace/queue cho trưởng ca), thêm `_customer_auto_refund_today_vnd` (tách `ledger_seed` như `T-OLD-1017` khỏi trần hoàn tự động theo khách trong ngày) và `_gate_send_reply` (đồng bộ số tiền báo khách khớp sổ cái); cập nhật `Thẻ đã bốc: S8` và **C0** trong `templates/form-c-incident.md`.
- **Sử dụng trợ lý AI:** Có sử dụng trợ lý AI để rà soát codebase, phân tích ca biên `guards.py` / `S8`, viết code helper và tổng hợp nhật ký lệnh; thành viên tự kiểm chứng lại toàn bộ diff, trace, unit test và thao tác ký/chốt/Git.

### Bằng chứng

- **Commits:** `6b7d9fa` (`Sign acceptance criteria`), `ef13982` (A5 + Khối 2A), `750b524` (cổng vòng 1 `guards.py`), `5d6db0d` (`LAB 10: chốt cổng vòng 1, quyết định v1`, tạo `config/round1.lock` hash `61609d41...`), và commit vòng 2 cho thẻ `S8` _(sẽ cập nhật hash cuối + `check_submission --collect` ở CP5)_.
- **Mã lần chạy (`runs/`):**
  - Bộ nền: `R-base-before-20261118-152513-8e0db9`, `R-base-after-20261118-160135-c03300`, `R-base-prepared-20261118-163042-66140c`, `R-base-after-20261118-172236-724204`, `R-base-after-20261118-174630-2cc72a` (`110/110`, `pass_rate 1.0`, `pass_k 1.0`, `ROI 0.72`).
  - Thẻ `S8`: `R-S8-before-20261118-164231-66140c` (`pass_rate 0.8654`, `wrongful_refund_vnd 6845000`, `35` lỗi hãng oan), `R-S8-prepared-20261118-164232-66140c` (`1.0`), `R-S8-after-20261118-172236-724204`, `R-S8-after-20261118-174629-2cc72a` (`260/260`, `pass_rate 1.0`, `pass_k 1.0`, `wrongful_refund_vnd 0`, `ROI 1.83`), `R-S8-grade-20261118-174630-2cc72a` (`code_hash 2cc72ab74861`).
- **Phiếu:** `A5` (`templates/form-a-criteria.md`), `B0#1–3` & `B7.1` (`templates/form-b-evaluation-gates.md`), `Thẻ đã bốc: S8` & `C0` (`templates/form-c-incident.md`).

### Exit ticket

- **Điều học được:** Cổng kiểm tra cấp hệ thống bên ngoài model (`guards.py` + `operating_gates.json`) không chỉ ngăn thất thoát tài chính mà còn hiệu chỉnh lại niềm tin người duyệt bằng lý do minh bạch (`_approval_failure_reasons` + `decision_note`), giúp giảm kiểm tay 100% xuống kiểm mẫu 10% mà vẫn giữ 0 ca hỏng.
- **Điều còn chưa chắc:** Cần tiếp tục kiểm chứng ở bộ test ẩn và môi trường pilot thật liệu còn trường hợp phê duyệt/thu hồi ngoài hệ thống chưa kịp đồng bộ DB `approvals` hoặc chia nhỏ qua nhiều `customer_id` khác nhau hay không trước khi sang Gate 2.

---

## VuTriDung-2A202603478

### Phần việc phụ trách

- **Vai trong bàn:** Kỹ sư cổng 2 (Chủ sở hữu `lab10/monitors.py`, Đo lường, Behavioral Test & Fault Tree)
- **File độc quyền sửa:** `lab10/monitors.py`.
- **Đầu ra bàn giao:** Gửi văn bản `A2(Offline), A3` cho TV3; `B1, B2, B7.2, B7.3` cho TV3; `C2, C6, C7, C8, C9` cho TV4; gửi 2 câu lệnh `--adhoc` cho TV1 chạy thử.
- **Chi tiết từng chặng:**
  - **Phút 0–15 (CP1):** Đọc `lab10/helpers.py`, `lab10/ops.py`, `data/world.json`.
  - **Phút 15–65 (Khối 1):** Làm **Câu 1.3** (`A2` cột Offline — thiết kế 1 offline metric cho 1 bước của agent) và **Câu 1.5** (`A3` — phân tích khoảng tin cậy 95%); soát công thức số liệu `ops_facts`/`ops_limits` và JSON `acceptance_criteria.json` cho TV3 (**Câu 1.6**); phác thảo sẵn khung hàm giám sát cho `monitors.py` & 2 kịch bản `--adhoc` từ `world.json`; phút 60–65 chạy `criteria verify` kiểm tra hash.
  - **Phút 65–115 (Khối 2):** Hoàn thiện phân tích tự chặn vs người duyệt ở **B1**; viết hướng xử lý & tín hiệu theo dõi ở **B2** (`Câu 2.2`); tham gia Pre-mortem **B6** (lăng kính Kỹ thuật); viết **Câu 2.7** (`B7.2` — 2 bước chống rò rỉ dữ liệu); hoàn thiện **Câu 2.8** (`B7.3` — 1 tính chất behavioral test + 2 ticket `--adhoc` phối hợp TV1 chạy & TV3 ra đề); viết sẵn monitor nền trong `lab10/monitors.py`; kiểm tra không ca nền nào mới hỏng ở `prepared`.
  - **Phút 125–200 (Khối 3):** Từ log trace của TV1 hoàn thiện **C2** (tác hại của thẻ, ≥ 2 lỗi khác nguồn, ≥ 1 lỗi chìm); chủ trì vẽ **Câu 3.4** (`C6` Fault tree TRƯỚC khi sửa — ≥ 2 nhánh ở ≥ 2 tầng khác nhau có bằng chứng); **Câu 3.6** (thêm ≥ 1 hàm mới đăng ký vào `MONITORS` trong `lab10/monitors.py`, điền bảng **C8** gồm thước đo, dữ liệu, cách tính, ngưỡng báo động, điểm mù, giá trị base/thẻ); tổng hợp bảng sửa **C7**; vẽ **C9** (Fault tree SAU khi sửa).
  - **Phút 200–240 (Demo & Nộp):** Demo trực tiếp 2 ticket hiểm `--adhoc` và chỉ số `monitors.py` khi phản biện; gửi phần cá nhân `TEAM.md` cho TV1 và tự nộp link repo trên LMS.

### Đóng góp cụ thể

_(Điền thực tế đã làm, và ghi rõ phần nào có sử dụng trợ lý AI nếu có.)_

### Bằng chứng

_(Điền mã commit, mã lần chạy_ `runs/<mã>`_, dòng trong phiếu.)_

### Exit ticket

_(Một điều học được, một điều còn chưa chắc.)_

---

## HoVaTen3-MSSV3

### Phần việc phụ trách

- **Vai trong bàn:** Sản phẩm và kinh doanh (**Form Keeper Phiếu A & Phiếu B**)
- **File độc quyền sửa:** `config/acceptance_criteria.json` _(chốt ở phút 60)_, `templates/form-a-criteria.md`, `templates/form-b-evaluation-gates.md`.
- **Đầu ra bàn giao:** Gửi 4 con số `business` (Vòng 1 & Vòng 2) cho TV4 nhập vào `config/operating_gates.json`; gửi `C4`, `3.2(C5)`, `C10`, `C12` + 3 dòng `three_lines` cho TV4 đưa vào Phiếu C & `submission.json`.
- **Chi tiết từng chặng:**
  - **Phút 0–15 (CP1):** Chọn **1 Eval card và 1 PRD v1.1 từ Lab 9** làm tài liệu chung của bàn.
  - **Phút 15–65 (Khối 1 · CP2):** Làm **Câu 1.1** (`A1` — mục tiêu cấp hệ thống theo PRD v1.1 §3); làm **Câu 1.6** (`A4` — câu tiêu chí "Nếu … thì …", 2 ranh giới đầu ra, soát 4 câu hỏi Bước 2, chốt `business_ops`, hẹn ngày xem lại) và điền `config/acceptance_criteria.json` (khớp tên `team` = `K5-L3A-DAY10-ComVoHan-PoCtoPilotGate1`, không chép ngưỡng từ file mẫu); nhận `1.2`–`1.5` từ TV2/TV4 để hoàn thiện `templates/form-a-criteria.md` trước khi TV1 ký ở phút 60. _(Sau khi ký không mở/lưu lại_ `acceptance_criteria.json`_)_.
  - **Phút 65–115 (Khối 2 · CP3):** Làm **Câu 2.3** (`B3` — Bản đồ dữ liệu 9 dòng + tóm tắt + ví dụ drift 3 tháng tới); điều phối Pre-mortem **Câu 2.5** (`B6` — lăng kính Kinh doanh & chốt 2–3 cổng); phối hợp TV2 ra đề 2 ticket hiểm **Câu 2.8**; làm **Câu 2.9** (`B7.4` — lý do có số từ `ops_limits`/`ops_facts` và gửi 4 số `business` cho TV4 nhập JSON); gom các mục từ TV1/TV2/TV4 vào `templates/form-b-evaluation-gates.md`; phút 105–115 chủ trì điền **B8 Quyết định Gate 1 · v1** cùng cả bàn chốt.
  - **Phút 125–200 (Khối 3):** Mở lại Pre-mortem **C1** (lăng kính Kinh doanh); làm **C4** (HAZOP của thẻ ≥ 3 dòng) và **Câu 3.2** (`C5` — 1 specification kiểm được bằng code/report); bổ sung nhánh kinh doanh vào **C6**; đề xuất chỉnh `business` (`pilot_scope`, trần, ngân sách) cho TV4 sửa `operating_gates.json` (và phối hợp TV2 nếu bốc thẻ `S5` về chi phí theo kho); viết **C10** (Risk register ≥ 1 dòng gắn với metric trong `monitors.py`/report); chủ trì viết **C12 Quyết định Gate 1 · v2**, mục "Chỉ ở v2" và **3 dòng bắt buộc**.
  - **Phút 200–240 (Demo & Nộp):** Trình bày bài toán kinh doanh, chi phí/ROI, phạm vi pilot và lập luận quyết định `v2` lúc demo; gửi phần cá nhân `TEAM.md` cho TV1 và tự nộp link repo trên LMS.

### Đóng góp cụ thể

_(Điền thực tế đã làm, và ghi rõ phần nào có sử dụng trợ lý AI nếu có.)_

### Bằng chứng

_(Điền mã commit, mã lần chạy_ `runs/<mã>`_, dòng trong phiếu.)_

### Exit ticket

_(Một điều học được, một điều còn chưa chắc.)_

---

## PhamTrungKien-2A202603479

### Phần việc phụ trách

- **Vai trong bàn:** Vận hành và pháp lý (**Chủ sở hữu** `config/operating_gates.json` **· Form Keeper Phiếu C ·** `submission.json`) · Họ tên: Phạm Trung Kiên · MSSV: `2A202603479`
- **File độc quyền sửa:** `config/operating_gates.json` _(cả 3 nhóm_ `business`_,_ `operations`_,_ `legal`_)_, `templates/form-c-incident.md`, `submission/submission.json`.
- **Đầu ra bàn giao:** Gửi `1.2`, `1.4` cho TV3 vào Phiếu A; gửi `B4`, `B5`, `B7.5`, `B7.6` cho TV3 vào Phiếu B; giao `config/operating_gates.json`, `form-c-incident.md`, `submission.json` sạch lỗi cho TV1 chạy `checkpoint` / `grade` / `--collect`.
- **Chi tiết từng chặng:**
  - **Phút 0–15 (CP1):** Thu thập họ tên + MSSV của 4 thành viên gửi TV1 điền `TEAM.md`; đọc mẫu `submission/submission.json`.
  - **Phút 15–65 (Khối 1):** Làm **Câu 1.2** (`A1` — góc nhìn chị Oanh `NV-OANH` và chị Hạnh `NV-HANH` từ PRD §2, §6 & `data/world.json`) và **Câu 1.4** (`A2` cột Telemetry production — thêm khung thời gian, ngưỡng báo động, điểm mù), gửi TV3 trước phút 55; trong thời gian còn lại **dựng trước khung Checklist 9 nhóm (**`B5`**), bản nháp thông số** `operations`**/**`legal` **(**`staff`**,** `ops_limits`**) và khung Runbook 1–3 (**`B7.5`**)**.
  - **Phút 65–115 (Khối 2 · CP3):** Hoàn thiện **Câu 2.4** (**B4** HAZOP vòng 1 ≥ 3 dòng + ≥ 2 dòng ngoài kỹ thuật; **B5** Checklist go-live 9 nhóm có PIC có tên từng dòng); tham gia Pre-mortem **B6** (lăng kính Con người/Vận hành & Pháp lý); làm **Câu 2.10** — điền toàn bộ `config/operating_gates.json` (gồm `business` nhận từ TV3 + `operations` & `legal`), viết **B7.5** (Runbook 1–3 khớp con số config, ghi rõ thời hạn dừng tối đa & người bấm) và **B7.6** (Giờ cao điểm); gửi toàn bộ mục trên cho TV3 dán vào Phiếu B trước phút 105. Phút 105–115: rà khớp 100% con số giữa `operating_gates.json` và Runbook 1–3.
  - **Phút 125–200 (Khối 3 · CP4–CP5):** Phút 125: ghi đúng số thẻ vào dòng `Thẻ đã bốc:` ở đầu `templates/form-c-incident.md` và `TEAM.md`; gom `C0#1`, `C1` (Pre-mortem & vượt trần vận hành mốc `prepared`); làm **C3** (phần riêng theo đúng số thẻ đã bốc; _thẻ_ `S8` → `C3.4` + một dòng “hoàn trên hạn mức” ở `C3.1`) và **Câu 3.3** (`C5` — 1 giả định môi trường ngầm tin có thể sai); bổ sung nhánh vận hành/pháp lý vào **C6**; sửa `config/operating_gates.json` theo hướng xử lý vòng 2 (`Câu 3.5`); viết **C11** (cập nhật Checklist 9 nhóm có PIC + Runbook phần 4–5); gom đủ `C0`–`C12` vào `templates/form-c-incident.md`; điền hoàn chỉnh `submission/submission.json` (`team`, `members` dạng `"HoVaTen-MSSV"` khớp `TEAM.md`, `incident`, `decision_v1`, `decision_v2`, chép nguyên `three_lines` từ `C12`) để TV1 chạy `check_submission --collect` tới `ĐỦ THÀNH PHẦN`.
  - **Phút 200–240 (Demo & Nộp):** Trình bày phần nhân sự trực, niềm tin người duyệt, pháp lý bên thứ ba và runbook lúc demo; gửi phần cá nhân `TEAM.md` cho TV1 và tự nộp link repo trên LMS.

### Đóng góp cụ thể

- **Khối 1:** Viết **Câu 1.2** (góc nhìn `NV-OANH` / `NV-HANH`) và **Câu 1.4** (telemetry production: cửa sổ 24 giờ, ngưỡng vàng/đỏ, điểm mù), gửi TV3 gom vào Phiếu A trước khi ký tiêu chí.
- **Khối 2 · CP3:** Hoàn thiện **B4** (HAZOP vòng 1, gồm ≥ 2 dòng ngoài kỹ thuật) và **B5** (checklist 9 nhóm có PIC); tham gia Pre-mortem **B6** (lăng kính Con người/Vận hành & Pháp lý); điền độc quyền `config/operating_gates.json` (`business` theo số TV3 chốt ở B7.4: trần hoàn ngày `1000000`, LLM/ticket `1100`, `pilot_scope all/100%`, `roi_min 0.3`; `operations`: PIC `NV-TUNG`, duyệt `NV-HANH`, `2` người trực / `12` ca/giờ, SLA `60` phút, `decision_note = true`, kiểm mẫu `10%`, `stop_conditions`, kênh Slack; `legal`: chặn PII + `carrier_fault_requires_recorded_cause = true`); viết **B7.5** Runbook 1–3 và **B7.6** Giờ cao điểm, rồi rà khớp 100% số với JSON.
- **CP4 (thẻ `S8`):** Ghi `Thẻ đã bốc: S8` vào đầu Phiếu C & `TEAM.md`; gom **C0#1** và điền **C1** (mã `grade`/`base`/`prepared`, cổng vòng 1 đỡ gì trên S8, vượt trần prepared, đối chiếu lại B6 + 1 lý do thiếu về phê duyệt INVALID).
- **Sử dụng trợ lý AI:** Có dùng trợ lý AI để soạn nháp `operating_gates.json`, Runbook B7.5–B7.6, đối chiếu số JSON↔Runbook và điền C1; tự đọc lại / chỉnh cho khớp `ops_limits`, B7.4 của TV3 và report S8.

### Bằng chứng

- **Commits liên quan:** `3c52638` (B4/B5), `327cad3` (B6), `bac1edf` (done 2.10 / operating gates + runbook), các chỉnh sync B7.4↔JSON↔Runbook (working tree), và phần `Thẻ đã bốc: S8` + **C1** trên `templates/form-c-incident.md` / `TEAM.md` _(chưa commit nếu còn đang mở)_.
- **Config:** `config/operating_gates.json` — `daily_refund_cap_vnd=1000000`, `cost_budget_per_ticket_vnd=1100`, `pilot_scope.mode=all`, `roi_min=0.3`, `reviewers_on_shift=2`, `review_capacity_per_hour=12`, `max_queue_wait_minutes=60`, `review_sampling_pct=10`, `decision_note=true`.
- **Mã lần chạy dùng cho C0#1 / C1:** `R-S8-grade-20261118-164230-66140c`, `R-S8-before-20261118-164231-66140c`, `R-S8-prepared-20261118-164232-66140c` (prepared: `pass_rate 1.0`, hoàn sai `0`, lỗi oan `0`, niềm tin duyệt **đạt**, ROI `1.83`).
- **Phiếu:** `A1`/`A2` (1.2, 1.4), `B4`, `B5`, `B7.5`, `B7.6` trong `templates/form-b-evaluation-gates.md`; `Thẻ đã bốc: S8`, **C0#1**, **C1** trong `templates/form-c-incident.md`.

### Exit ticket

- **Điều học được:** Niềm tin người duyệt không sửa được chỉ bằng “chặn tiền”; phải khớp bộ ba `decision_note` + kiểm mẫu + `approver_id` đúng người đứng tên với `stop_conditions`/`alert_channel` trong runbook, thì mới hạ được kiểm tay 100% xuống kiểm mẫu mà không ùn hàng chờ.
- **Điều còn chưa chắc:** Sau vòng 2 S8, chưa chắc các biến thể phê duyệt INVALID (dùng lại / hết hạn / thu hồi / vượt `max_vnd`) đã được cover hết ở test ẩn, và `operating_gates.json` còn cần chỉnh thêm nhân sự/trần nào trước khi chốt **C11** + `submission.json`.
