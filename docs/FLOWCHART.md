# 流程圖與系統流程設計 - 校園惜食匹配系統

本文件根據產品需求文件 (PRD) 與系統架構設計 (ARCHITECTURE)，視覺化使用者的操作路徑與後端資料流。

## 1. 使用者流程圖（User Flow）

以下流程圖說明不同角色（學生需求端、餐廳供應端）在系統上的主要操作路徑。

```mermaid
flowchart LR
    Start([進入網站]) --> Home[首頁 & 統計看板]
    
    Home --> CheckAuth{是否已登入？}
    CheckAuth -->|否| Auth[登入/註冊頁面]
    CheckAuth -->|是| RoleCheck{使用者身份}
    
    Auth --> RoleCheck
    
    %% 學生端流程
    RoleCheck -->|在校學生| StudentHome[學生儀表板 / 剩食即時地圖]
    StudentHome --> ViewFood[瀏覽剩食列表與詳情]
    ViewFood --> ActionReserve[點擊預約取餐]
    ActionReserve --> ConfirmReserve[確認預約並產生存根]
    ConfirmReserve --> MyOrders[查看我的預約]
    
    %% 餐廳端流程
    RoleCheck -->|餐廳業者| RestHome[餐廳管理後台]
    RestHome --> RestAction{選擇操作}
    
    RestAction -->|發佈剩食| AddFood[填寫剩食表單]
    AddFood --> SaveFood[完成上架與設定下架時間]
    SaveFood --> RestHome
    
    RestAction -->|管理現有剩食| EditFood[修改或刪除剩食]
    EditFood --> RestHome
    
    RestAction -->|處理學生取餐| ManageOrders[查看預約清單]
    ManageOrders --> VerifyOrder[核銷確認取餐]
    VerifyOrder --> RestHome
```

---

## 2. 系統序列圖（Sequence Diagram）

以下列出核心功能：「餐廳業者新增剩食」從前端操作到後端資料庫儲存的完整交互流程。

```mermaid
sequenceDiagram
    actor User as 餐廳業者
    participant Browser as 瀏覽器 (Frontend)
    participant Flask as Flask Route (Controller)
    participant Model as Food Model
    participant DB as SQLite 資料庫
    
    User->>Browser: 在發佈頁面填寫剩食資訊與上傳圖片
    User->>Browser: 點擊「確認發佈」
    Browser->>Flask: HTTP POST /foods/new (攜帶表單資料與圖片)
    
    %% 處理請求與圖片
    Flask->>Flask: 驗證使用者身份與權限
    Flask->>Flask: 儲存圖片至 static/images/uploads，並產生路徑
    
    %% 呼叫 Model
    Flask->>Model: 建立 Food 物件 (包含名稱、份量、圖片路徑、下架時間)
    Model->>DB: INSERT INTO foods ...
    DB-->>Model: 回傳成功與資料 ID
    Model-->>Flask: 回傳建立成功狀態
    
    Flask-->>Browser: HTTP 302 重導向到餐廳管理後台 (回傳成功訊息)
    Browser->>User: 顯示「發佈成功」並列出最新剩食
```

---

## 3. 功能清單對照表

本表列出系統主要功能及其對應的 URL 路徑規劃與使用的 HTTP 方法：

| 功能模組 | 功能描述 | URL 路徑 | HTTP 方法 |
| :--- | :--- | :--- | :--- |
| **首頁與統計** | 首頁與減碳/惜食量統計看板 | `/` | GET |
| **認證授權** | 使用者登入 (校內信箱驗證) | `/auth/login` | GET / POST |
| **認證授權** | 使用者註冊 | `/auth/register` | GET / POST |
| **認證授權** | 使用者登出 | `/auth/logout` | GET |
| **剩食 (餐廳端)** | 新增發佈剩食 (含上傳圖片) | `/foods/new` | GET / POST |
| **剩食 (餐廳端)** | 編輯或刪除剩食 | `/foods/<id>/edit` | GET / POST |
| **剩食 (學生端)** | 查看所有進行中的剩食 (列表與地圖) | `/foods` | GET |
| **剩食 (學生端)** | 檢視特定剩食詳細資訊 | `/foods/<id>` | GET |
| **預約 (學生端)** | 預約該項剩食 | `/foods/<id>/reserve` | POST |
| **預約 (學生端)** | 學生查看自己的預約紀錄 | `/orders/my` | GET |
| **預約 (餐廳端)** | 餐廳查看並核銷學生的預約訂單 | `/orders/manage` | GET / POST |
