from flask import Flask
from qunyin.ext import init_ext
from qunyin.views import init_blue

def create_app():
    app = Flask(__name__)
    #注册蓝图
    init_blue(app)
    #外部第三方扩展库
    init_ext(app)
    return app