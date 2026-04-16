from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def index():
    """
    首頁看板
    輸入: 無
    處理邏輯: 查詢系統整體減少的碳排量與餐點數量，返回統計資料。
    輸出: 渲染 index.html 首頁
    """
    pass
