import os
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from werkzeug.utils import secure_filename
from app.models.food import Food
from app.models.order import Order
from app.models import db

food_bp = Blueprint('food', __name__, url_prefix='/foods')

@food_bp.route('/', methods=['GET'])
def index():
    now = datetime.now()
    foods = Food.query.filter(Food.status == 'available', Food.portion > 0, Food.end_time > now).order_by(Food.created_at.desc()).all()
    return render_template('food/index.html', foods=foods)

@food_bp.route('/new', methods=['GET', 'POST'])
def new():
    if session.get('role') != 'restaurant':
        flash('只有餐廳業者可以發佈剩食！', 'warning')
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        portion = int(request.form.get('portion', 0))
        original_price = request.form.get('original_price')
        discount_price = request.form.get('discount_price')
        end_time_str = request.form.get('end_time')
        
        image_file = request.files.get('image')
        image_path = None
        if image_file and image_file.filename != '':
            filename = secure_filename(image_file.filename)
            upload_dir = os.path.join(current_app.root_path, 'static', 'images', 'uploads')
            os.makedirs(upload_dir, exist_ok=True)
            file_path = os.path.join(upload_dir, filename)
            image_file.save(file_path)
            image_path = f"images/uploads/{filename}"

        if not all([name, portion, end_time_str]):
            flash('必填欄位不可為空！', 'danger')
            return redirect(url_for('food.new'))

        end_time = datetime.strptime(end_time_str, '%Y-%m-%dT%H:%M')
        
        Food.create(
            restaurant_id=session['user_id'],
            name=name,
            description=description,
            portion=portion,
            original_price=int(original_price) if original_price else None,
            discount_price=int(discount_price) if discount_price else 0,
            image_path=image_path,
            end_time=end_time
        )
        flash('剩食發佈成功！', 'success')
        return redirect(url_for('order.manage')) 

    return render_template('food/new.html')

@food_bp.route('/<int:food_id>', methods=['GET'])
def detail(food_id):
    food = Food.get_by_id(food_id)
    if not food:
        flash('找不到該餐點', 'danger')
        return redirect(url_for('food.index'))
    return render_template('food/detail.html', food=food)

@food_bp.route('/<int:food_id>/edit', methods=['GET', 'POST'])
def edit(food_id):
    if session.get('role') != 'restaurant':
        flash('權限不足', 'danger')
        return redirect(url_for('food.index'))

    food = Food.get_by_id(food_id)
    if not food or food.restaurant_id != session['user_id']:
        flash('您無權編輯此資料', 'danger')
        return redirect(url_for('order.manage'))

    if request.method == 'POST':
        food.name = request.form.get('name')
        food.description = request.form.get('description')
        food.portion = int(request.form.get('portion', 0))
        food.original_price = request.form.get('original_price', type=int)
        food.discount_price = request.form.get('discount_price', type=int)
        
        end_time_str = request.form.get('end_time')
        if end_time_str:
            try:
                food.end_time = datetime.strptime(end_time_str, '%Y-%m-%dT%H:%M')
            except ValueError:
                # 處理沒有秒數或不同格式的情況 (部分瀏覽器支援度差異)
                pass
                
        db.session.commit()
        flash('更新成功', 'success')
        return redirect(url_for('order.manage'))

    return render_template('food/edit.html', food=food)

@food_bp.route('/<int:food_id>/delete', methods=['POST'])
def delete(food_id):
    if session.get('role') != 'restaurant':
        return redirect(url_for('main.index'))
        
    food = Food.get_by_id(food_id)
    if food and food.restaurant_id == session['user_id']:
        food.delete()
        flash('已成功刪除該筆資料', 'info')
    return redirect(url_for('order.manage'))

@food_bp.route('/<int:food_id>/reserve', methods=['POST'])
def reserve(food_id):
    if session.get('role') != 'student':
        flash('只有學生身份可以預約餐點！請登入學生帳號。', 'warning')
        return redirect(url_for('auth.login'))

    quantity = int(request.form.get('quantity', 1))
    food = Food.get_by_id(food_id)

    if not food or food.status != 'available':
        flash('餐點已下架或完售', 'danger')
        return redirect(url_for('food.index'))

    if food.portion < quantity:
        flash('抱歉，庫存不足！', 'warning')
        return redirect(url_for('food.detail', food_id=food.id))

    food.portion -= quantity
    if food.portion == 0:
        food.status = 'out_of_stock'
        
    Order.create(
        student_id=session['user_id'],
        food_id=food.id,
        quantity=quantity
    )
    
    db.session.commit()
    
    flash('預約成功！別忘了在時間內前往取餐。', 'success')
    return redirect(url_for('order.my_orders'))
