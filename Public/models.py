import datetime

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

'''
    数据库初始化
'''
def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()


class Person(db.Model):
    p_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    p_name = db.Column(db.String(16))
    # Sqlite 不支持👇这种方式
    # #默认值
    # del_num = db.Column(db.Integer, default=1)
    # # 时间
    # tijiao_time = db.Column(db.DateTime, default=datetime.datetime.now)
    # #枚举
    # status = db.Column(db.Enum('0', '1', '2', '3'), server_default='0')


class Tg(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)

class AliWebhook(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    rules = db.Column(db.String())
    instanceId = db.Column(db.String())
    msgid = db.Column(db.String())
    transId = db.Column(db.String())
    timestamp = db.Column(db.String())

class AliWebhook_white(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    rules = db.Column(db.String())
    instanceId = db.Column(db.String())
    isall = db.Column(db.Integer()) #是否全部屏蔽 1是全部屏蔽 0是单个规则屏蔽