from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

'''
    tg表
'''
def init_db(app):
    db.init_app(app)