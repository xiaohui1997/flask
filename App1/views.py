from flask import Blueprint, render_template, abort, url_for, request, make_response, redirect, jsonify
from jinja2 import TemplateNotFound

rc = Blueprint('rc', __name__,
                        template_folder='templates') #蓝图名称,导入的名称


@rc.route('/haha2/') #请注意在蓝图中路由不可一样,否则会覆盖掉之前的路由
def haha1():
    return 'okok'


@rc.route('/html/')
def haha():
    return render_template('before/index.html'),403
