from flask import Blueprint, render_template, request, redirect, url_for, session

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    登入功能
    輸入: POST 時帶有 email, password 表單參數
    處理邏輯: 
      - GET: 返回登入表單
      - POST: 驗證使用者憑證，成功後記錄 session，依 role 重導向
    輸出: 渲染 auth/login.html 或 重導向首頁/後台
    """
    pass

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    註冊功能
    輸入: POST 帶有 email, password, name, role 等
    處理邏輯: 
      - GET: 返回註冊表單
      - POST: 建立 User 資料，並導向登入頁面
    輸出: 渲染 auth/register.html 或重導向 /auth/login
    """
    pass

@auth_bp.route('/logout', methods=['GET'])
def logout():
    """
    登出功能
    輸入: 無
    處理邏輯: 清除 session 中的使用者資訊
    輸出: 重導向到首頁 /
    """
    pass
