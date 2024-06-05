from flask import Blueprint, render_template, abort, url_for, request, make_response, redirect, jsonify
from jinja2 import TemplateNotFound

app1 = Blueprint('app1', __name__,
    static_folder='static', #静态文件夹
    template_folder='templates') #蓝图名称,导入的名称


@app1.route('/app1/') #请注意在蓝图中路由不可一样,否则会覆盖掉之前的路由
def haha1():
    return 'app1'