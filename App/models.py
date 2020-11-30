from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

def init_db(app):
    db.init_app(app)

class Person(db.Model):
    p_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    p_name = db.Column(db.String(16))
    #默认值
    del_num = db.Column(db.Integer, default=1)
    # 时间
    tijiao_time = db.Column(db.DateTime, default=datetime.datetime.now)
    #枚举
    status = db.Column(db.Enum('0', '1', '2', '3'), server_default='0')