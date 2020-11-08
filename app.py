"""Run the app locally

python app.py
"""
from application import create_app

if __name__ == '__main__':
    app = create_app('config.DevelopmentConfig')
    app.run(host='0.0.0.0', port='5001')
