import os
from flask import Flask
from app.models import db
from app.routes import register_blueprints

def create_app(test_config=None):
    # 初始化 Flask 應用程式並設定 instance 目錄存放套件內建相對路徑設定
    app = Flask(__name__, instance_relative_config=True)
    
    # 設定預設連線字串與開發用 Secret Key
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
        SQLALCHEMY_DATABASE_URI=os.environ.get(
            'DATABASE_URL', 
            'sqlite:///' + os.path.join(app.instance_path, 'database.db')
        ),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config is None:
        # 非測試環境時，嘗試讀取 instance/config.py 隱藏版設定
        app.config.from_pyfile('config.py', silent=True)
    else:
        # 測試環境專用設定
        app.config.from_mapping(test_config)

    # 確保 instance 目錄存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 初始化資料庫綁定
    db.init_app(app)

    # 為了方便開發，啟動時自動檢查並建立所有未存在的資料表
    with app.app_context():
        db.create_all()

    # 註冊所有在路由模組設計好的 Blueprints
    register_blueprints(app)

    return app
