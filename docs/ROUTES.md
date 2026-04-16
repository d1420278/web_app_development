# 路由與頁面設計文件 (Routes & Page Planning)

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| --- | --- | --- | --- | --- |
| 首頁與看板 | GET | `/` | `index.html` | 顯示首頁、減碳與惜食統計看板 |
| 登入頁面 | GET | `/auth/login` | `auth/login.html` | 顯示登入表單 |
| 處理登入 | POST | `/auth/login` | — | 驗證信箱與密碼，存入 session，重導向 |
| 註冊頁面 | GET | `/auth/register` | `auth/register.html` | 顯示註冊表單 |
| 處理註冊 | POST | `/auth/register` | — | 建立使用者，重導向登入頁面 |
| 登出 | GET | `/auth/logout` | — | 清除 session，重導向首頁 |
| 剩食列表 | GET | `/foods/` | `food/index.html` | 列出目前所有可用剩食（並顯示地圖） |
| 發佈剩食頁面 | GET | `/foods/new` | `food/new.html` | 顯示新增發佈表單（餐廳專用） |
| 處理發佈剩食 | POST | `/foods/new` | — | 儲存圖片與資料，重導向管理頁面 |
| 查看單筆剩食 | GET | `/foods/<int:food_id>` | `food/detail.html` | 查看剩食詳情 |
| 編輯剩食頁面 | GET | `/foods/<int:food_id>/edit`| `food/edit.html` | 顯示編輯表單（餐廳專用） |
| 處理編輯剩食 | POST| `/foods/<int:food_id>/edit`| — | 更新資料，重導向管理頁面 |
| 處理刪除剩食 | POST| `/foods/<int:food_id>/delete`| — | 刪除資料，重導向管理頁面 |
| 預約餐點 | POST| `/foods/<int:food_id>/reserve`| — | 學生預約剩食，檢查份量、存入預約表 |
| 學生預約紀錄 | GET | `/orders/my` | `order/my.html` | 顯示學生過去與目前的預約紀錄 |
| 餐廳管理訂單 | GET | `/orders/manage` | `order/manage.html`| 顯示餐廳收到、待核銷的預約清單 |
| 核銷訂單 | POST| `/orders/<int:order_id>/complete`| — | 將訂單狀態設為 completed（核銷完成） |

## 2. 每個路由的詳細說明

### Main (首頁模組)
- **GET `/`**
  - **輸入**: 無
  - **處理邏輯**: 取出系統內完成 (completed) 的訂單總數，估算減碳量展示於看板。
  - **輸出**: 渲染 `index.html`。

### Auth (認證模組)
- **POST `/auth/login`**
  - **輸入**: `email`, `password`
  - **處理邏輯**: 查詢 User 模型，比對密碼 hash。若正確，存入 Session 並根據 Role 導向（餐廳導到 `/orders/manage`，學生導到 `/foods/`）。
  - **出錯邏輯**: 若無效回傳 401 或提供 flash 錯誤訊息。
- **POST `/auth/register`**
  - **輸入**: `role`, `email`, `password`, `name`
  - **處理邏輯**: 驗證信箱規則，若學生檢查後綴。若正確，Hash 密碼並建立 User 紀錄。
  - **出錯邏輯**: 欄位缺漏或信箱已被使用，退回表單頁面並帶閃現警告。

### Food (剩食模組)
- **GET `/foods/`**
  - **輸入**: 搜尋與篩選 (Query Params Optional)
  - **處理邏輯**: 檢視過期狀態（`end_time` 逾期者隱藏），返回 `status='available'` 過濾後的結果供清單、地圖點位輸出。
- **POST `/foods/new`**
  - **輸入**: 表單提交（圖片、品名、原價/特價、份數、到期時間）
  - **處理邏輯**: 產生圖檔名稱並存檔於 `static/images/uploads`，呼叫 `Food.create(...)` 塞入資料。
- **POST `/foods/<id>/reserve`**
  - **輸入**: `quantity`
  - **處理邏輯**: 從 Session 抓學生身份。若該 Food `portion >= quantity` 且未逾期：
    - `Food.portion -= quantity`
    - `Order.create(student_id=..., food_id=..., quantity=...)`
  - **輸出**: Flash 預約成功並導向 `/orders/my`。

### Order (訂單模組)
- **GET `/orders/manage`**
  - **處理邏輯**: 餐廳視角，透過關聯找出 `Food.restaurant_id == current_user.id` 底下的所有訂單，依照狀態排序。
- **POST `/orders/<id>/complete`**
  - **處理邏輯**: 權限卡控後，調用 `Order.complete_order()` 修改訂單為 `completed` 與更新時間。導回 `/orders/manage`。

## 3. Jinja2 模板清單

所有的視圖模板皆繼承自底層框架 `base.html`，以保持響應式導航欄的一致性。

- `templates/base.html`: 共同版型、導覽列 (Navbar)、頁尾 (Footer)、Flash 訊息彈窗。
- `templates/index.html`: (繼承 base) 網站落地頁，主視覺與數據儀表板。
- `templates/auth/login.html`: (繼承 base) 登入畫面卡片。
- `templates/auth/register.html`: (繼承 base) 註冊畫面卡片。
- `templates/food/index.html`: (繼承 base) 學生端：剩食清單介面與即時 Leaflet.js 地圖。
- `templates/food/new.html`: (繼承 base) 餐廳端：剩食發佈表單（支援圖片預覽）。
- `templates/food/detail.html`: (繼承 base) 獨立剩食詳細資料，右側含有預約按鈕。
- `templates/food/edit.html`: (繼承 base) 餐廳端：更新剩食份數或時間。
- `templates/order/my.html`: (繼承 base) 學生端：QR Code 存根顯示或預約列表。
- `templates/order/manage.html`: (繼承 base) 餐廳端：後台表格，有「核銷確認」的快速按鈕。

## 4. 路由骨架程式碼
請參閱 `app/routes/` 檔案目錄中的骨架程式碼 (採用 Blueprint 結構開發)。
