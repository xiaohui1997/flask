from flask import Flask
from app.views import rc
from app1.views import app1

#from qunyin.ext import init_ext
#from qunyin.views import init_blue

def create_app():
    app = Flask(__name__)
    ####批量注册蓝图####
    #注册蓝图
    app.register_blueprint(rc)
    app.register_blueprint(app1)
    #init_blue(app)
    #外部第三方扩展库
    #init_ext(app)
    return app