from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash('請輸入信箱與密碼！', 'warning')
            return redirect(url_for('auth.login'))

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['role'] = user.role
            session['name'] = user.name
            flash(f'歡迎回來，{user.name}！', 'success')
            
            # 根據身份跳轉到不同頁面
            if user.role == 'restaurant':
                return redirect(url_for('order.manage'))
            else:
                return redirect(url_for('food.index'))
        else:
            flash('信箱或密碼錯誤，請重新確認！', 'danger')
            return redirect(url_for('auth.login'))

    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        role = request.form.get('role')
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')

        if not all([role, email, password, name]):
            flash('請填寫所有必填欄位！', 'warning')
            return redirect(url_for('auth.register'))

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('此信箱已經被註冊過！', 'danger')
            return redirect(url_for('auth.register'))

        # Hash 密碼處理
        hashed_pw = generate_password_hash(password)
        
        try:
            User.create(
                role=role,
                email=email,
                password_hash=hashed_pw,
                name=name
            )
            flash('註冊成功！麻煩請您重新登入。', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            flash(f'註冊發生錯誤：{str(e)}', 'danger')
            return redirect(url_for('auth.register'))

    return render_template('auth/register.html')

@auth_bp.route('/logout', methods=['GET'])
def logout():
    session.clear()
    flash('您已成功登出系統。', 'info')
    return redirect(url_for('main.index'))
