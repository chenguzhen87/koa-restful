import os
from app import create_app

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

if __name__ == '__main__':
    print("http://127.0.0.1:9090")
    app.run(host='0.0.0.0',port=9090,debug=True)