# _*_coding=utf8_*_
'''
 PYTHONIOENCODING=utf-8 python3 manage.py
 路由采取蓝图将路由分开写在不同文件
'''
import pymysql
import os
from Public import create_app
from Public.models import init_db
from Tg.tg import tg_main
#from flask_script import Manager # flask-script 插件 可以接受终端参数  --help  python manage.py runservere
#初始化蓝图
app = create_app()
#sqllite3 数据库连接
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite3.db'
#json 中文显示
app.config['JSON_AS_ASCII'] = False

#mysql 数据库连接
#Tg.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:xiaotang@192.168.144.107:3306/test1'
#Tg.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


#db初始化
db = init_db(app)

if __name__ == "__main__":
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        # 这些代码只会在工作进程中运行
        tg_main()
    app.run(port=8833, host="0.0.0.0", debug=True)
