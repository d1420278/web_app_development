from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models.food import Food
from app.models.order import Order
from app.models import db

order_bp = Blueprint('order', __name__, url_prefix='/orders')

@order_bp.route('/my', methods=['GET'])
def my_orders():
    if session.get('role') != 'student':
        flash('此頁面僅限學生帳號存取！', 'warning')
        return redirect(url_for('auth.login'))
        
    orders = Order.query.filter_by(student_id=session['user_id']).order_by(Order.created_at.desc()).all()
    return render_template('order/my.html', orders=orders)

@order_bp.route('/manage', methods=['GET'])
def manage():
    if session.get('role') != 'restaurant':
        flash('只有餐廳業者可進入管理後臺！', 'warning')
        return redirect(url_for('main.index'))
        
    # Find all orders linked to foods posted by this restaurant
    my_foods = Food.query.filter_by(restaurant_id=session['user_id']).order_by(Food.created_at.desc()).all()
    food_ids = [f.id for f in my_foods]
    
    if food_ids:
        reserved_orders = Order.query.filter(Order.food_id.in_(food_ids), Order.status == 'reserved').order_by(Order.created_at.desc()).all()
        completed_orders = Order.query.filter(Order.food_id.in_(food_ids), Order.status == 'completed').order_by(Order.completed_at.desc()).limit(15).all()
    else:
        reserved_orders = []
        completed_orders = []
    
    return render_template('order/manage.html', foods=my_foods, reserved_orders=reserved_orders, completed_orders=completed_orders)

@order_bp.route('/<int:order_id>/complete', methods=['POST'])
def complete(order_id):
    if session.get('role') != 'restaurant':
        return redirect(url_for('main.index'))
        
    order = Order.get_by_id(order_id)
    if order and order.food.restaurant_id == session['user_id'] and order.status == 'reserved':
        order.complete_order() 
        flash(f'預約單 #{order.id} 已經成功核銷！', 'success')
        
    return redirect(url_for('order.manage'))
