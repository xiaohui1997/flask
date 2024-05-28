from flask import Blueprint, render_template, abort, url_for, request, make_response, redirect, jsonify
from jinja2 import TemplateNotFound
from  Public.models import db, Tg

rc = Blueprint('app', __name__,
    static_folder='static', #静态文件夹
    template_folder='templates') #蓝图名称,导入的名称


@rc.route('/app/') #请注意在蓝图中路由不可一样,否则会覆盖掉之前的路由
def haha1():
    new_person = Tg(id=123)
    db.session.add(new_person)
    db.session.commit()
    return 'app'


@rc.route('/html/')
def haha():
    # return render_template('before/index.html')
    return 'app1',403