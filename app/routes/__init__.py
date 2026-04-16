def register_blueprints(app):
    """
    註冊專案所有的 Blueprint 供 Flask App 使用。
    """
    from .main import main_bp
    from .auth import auth_bp
    from .food import food_bp
    from .order import order_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(food_bp)
    app.register_blueprint(order_bp)
