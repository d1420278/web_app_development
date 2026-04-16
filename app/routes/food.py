from flask import Blueprint, render_template, request, redirect, url_for, session

food_bp = Blueprint('food', __name__, url_prefix='/foods')

@food_bp.route('/', methods=['GET'])
def index():
    """
    剩食列表與地圖
    輸入: 無 (可選過濾條件如區域、價格排序)
    處理邏輯: 取得所有 status='available' 且未逾期的 Food，回傳給模板
    輸出: 渲染 food/index.html
    """
    pass

@food_bp.route('/new', methods=['GET', 'POST'])
def new():
    """
    新增剩食發佈
    輸入: POST 帶有表單 (name, portion, price, end_time, image)
    處理邏輯: 
      - 限定餐廳身份
      - GET: 返回發佈剩食表單
      - POST: 儲存圖片，建立 Food，關聯目前餐廳的 ID
    輸出: 渲染 food/new.html 或 重導向到管理後台
    """
    pass

@food_bp.route('/<int:food_id>', methods=['GET'])
def detail(food_id):
    """
    檢視剩食詳情
    輸入: food_id 路徑參數
    處理邏輯: 根據 ID 找出對應剩食與剩餘狀況
    輸出: 渲染 food/detail.html
    """
    pass

@food_bp.route('/<int:food_id>/edit', methods=['GET', 'POST'])
def edit(food_id):
    """
    編輯剩食資訊
    輸入: food_id 及 POST 表單資料
    處理邏輯: 
      - 限定為該餐廳擁有者
      - GET: 顯示目前資料在表單上
      - POST: 更新 Food 內容 (價格、份量或下架時間)
    輸出: 渲染 food/edit.html 或重導向 /foods/<food_id>
    """
    pass

@food_bp.route('/<int:food_id>/delete', methods=['POST'])
def delete(food_id):
    """
    刪除剩食
    輸入: food_id
    處理邏輯: 確認餐廳權限，執行軟刪除或直接刪除 Database 紀錄
    輸出: 重導向到首頁或餐廳後台
    """
    pass

@food_bp.route('/<int:food_id>/reserve', methods=['POST'])
def reserve(food_id):
    """
    預約剩食
    輸入: food_id 及隱藏/選定的數量 quantity
    處理邏輯: 
      - 限定學生身份登入
      - 判斷剩餘 portion 是否足夠
      - 建立 Order 記錄並扣除 Food 的 portion
    輸出: 重導向到 /orders/my 或單一訂單明細
    """
    pass
