from app import create_app

# 根據 __init__.py 內的 factory pattern 產生 app 實例
app = create_app()

if __name__ == '__main__':
    # 執行伺服器 (若為本地開發直接執行此檔時會使用 5000 port)
    app.run(debug=True, host='0.0.0.0', port=5000)
