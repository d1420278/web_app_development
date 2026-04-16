from flask import Blueprint, render_template, request, redirect, url_for, session

order_bp = Blueprint('order', __name__, url_prefix='/orders')

@order_bp.route('/my', methods=['GET'])
def my_orders():
    """
    學生預約紀錄列表
    輸入: 無
    處理邏輯: 讀取當前 Session 中的 user_id，取得建立的所有 Orders
    輸出: 渲染 order/my.html
    """
    pass

@order_bp.route('/manage', methods=['GET'])
def manage():
    """
    餐廳管理訂單後台
    輸入: 無
    處理邏輯: 取得當前餐廳所擁有的 Foods 中的相關被預約 Orders 資訊
    輸出: 渲染 order/manage.html
    """
    pass

@order_bp.route('/<int:order_id>/complete', methods=['POST'])
def complete(order_id):
    """
    核銷訂單操作
    輸入: order_id
    處理邏輯: 限定餐廳身份，調用 Model 將訂單狀態改為 'completed' 並寫入 completed_at 時間戳記
    輸出: 重導向到 /orders/manage 以重新載入頁面
    """
    pass
