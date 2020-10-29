from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

simple_page1 = Blueprint('simple_page1', __name__,template_folder='templates')


@simple_page1.route('/haha1')
def haha():
    return 'haha1'

#模板渲染
@simple_page1.route('/html/')
def html():
    return render_template('before/index.html')