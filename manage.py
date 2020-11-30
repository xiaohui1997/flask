# _*_coding=utf8_*_
'''
 PYTHONIOENCODING=utf-8 python3 manage.py
 路由采取蓝图将路由分开写在不同文件
'''
import pymysql
from flask import Flask
from Public import create_app
from App.models import init_db
from flask_script import Manager # flask-script 插件 可以接受终端参数  --help  python manage.py runservere
#初始化蓝图
app = create_app()
#sqllite3 数据库连接
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite3.db'
#mysql 数据库连接
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:xiaotang@192.168.144.107:3306/test1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#APP蓝图
#from App.views import simple_page
#app.register_blueprint(simple_page) #注册蓝图

#APP1蓝图
#from App1.views import rc
#app.register_blueprint(rc) #注册蓝图


manager = Manager(app=app)

#db初始化
init_db(app)



if __name__ == "__main__":
    #app.run()
    manager.run()
