import random
from App.models import *
from flask import Blueprint, render_template, abort, url_for, request, make_response, redirect, jsonify, Response, session
from jinja2 import TemplateNotFound

simple_page = Blueprint('simple_page', __name__,
                        template_folder='templates') #蓝图名称,导入的名称

# @simple_page.route('/', defaults={'page': 'index'})
# @simple_page.route('/<page>')
# def show(page):
#     try:
#         return render_template('pages/%s.html' % page)
#     except TemplateNotFound: #404 异常处理
#         #abort(404)
#         return 'im is test'


@simple_page.route('/haha1')
def haha1():
    return 'haha1'


@simple_page.route('/haha')
def haha():
    return 'haha'


#获取路径/位置参数 string int float path(字符串,会将/认为是一个字符) uuid(验证uuid用) any（any(c,d,e):an)枚举
@simple_page.route('/hello/<int:hehe>/', methods=['GET','POST']) #GET POST DELETE PUT HEAD
def hello(hehe,oo=22):
    print(hehe)
    return '路径参数'

#url_for 反向解析  根据函数名获取路径
@simple_page.route('/url/')
def url():
    print(url_for('simple_page.haha')) #因为使用了蓝图所以需要带上simple_page.
    print(url_for('simple_page.haha',an='sd',key='value'))  # 带参数写法
    return '反向解析'

#request 请求
@simple_page.route('/request/')
def request():
    '''
    request.method
    request.data  二进制数据byte类型
    request.args  get请求参数
    request.form  post相关请求都会有数据
    request.files 文件相关
    request.cookies
    request.remote_addr
    request.json
    request.user_agent
    request.host  url
    '''
    print(request.args['name'])  #不建议使用,如果参数不存在会报错
    print(request.args.get('name')) #不报错,没有返回None,有就直接返回值
    print(request.args.getlist('name')) #获取列表[]

    return '请求'
    pass

#响应 response
@simple_page.route('/response/')
def response():
    result = render_template('hello.html') #返回一个html页面  templates/hello.html
    response = make_response('<h2>test</h2>',400) #返回一个自定义response对象 400状态码
    response = make_response(result,400) #返回一个自定义response对象 400状态码
    return result,401 #配置状态码  401 客户端错误 400 关闭连接
    pass

#重定向操作
@simple_page.route('/redirect/')
@simple_page.route('/redire')  #可以定义多个路由
def redir():
    #abort(405)  #直接终止  方法不被支持
    return jsonify({'name':'value'})  #返回json数据  json格式化
    return redirect(url_for('simple_page.url')) #url_for 反向解析

#会话技术
'''
cookie
客户端会话技术
数据都是存储在浏览器中
支持过期
不能跨域名
frame标签
可以直接加载整个网站
不能跨浏览器
cookie是通过response来进行操作
flask 中的cookie 可以直接支持中文

resp = Response(response='登录成功%s' % username)
#设置cookie
resp.set_cookie('user',username)
#删除cookie
resp.delete_cookie('user')

session #存放内存中/nosql数据库
Flask-Session
app.config['SESSION_TYPE'] = 'redis' #放入redis中
Session(app=app)
#存
session['user'] = username
#取
username = session.get('user')
#设置secret key
app.config['SECRET_KEY'] = '12321KASLDJFALSFKDJKSA' #值随便写
token
'''

#关系型数据库
#flask-sqlalchemy
@simple_page.route('/createdb/')
def createdb():
    db.create_all()
    return 'DB Create Suncce'
    pass

 #数据库插入数据
@simple_page.route('/addperson/')
def add_person():
    p = Person()
    p.p_name = '热爱的看法%d' % random.randrange(100)
    db.session.add(p)
    db.session.commit()
    return 'Person Add Success'
    pass

#数据库插入多条数据
@simple_page.route('/addmultiple/')
def addmultiple():
    students = []
    for i in range(10)
        student = Person()
        student.p_name = "爱小明%d" % random.randrange(100)
        stundents.append(students)
    db.session.add_all(students)
    db.session.commit()
    #批量添加数据2
    # c = Pen()
    # types = ["铅笔","画笔","刷笔"]
    # #批量添加数据
    # objects = [Pen(name=types[0],type=str(data['qianbi'])), Pen(name=types[1],type=str(data['huabi'])), Pen(name=types[2],type=str(data['shuabi']))]
    # db.session.add_all(objects)
    # try:
    #     db.session.commit()
    # except Exception:
    #     pass
    
#更新多条数据
@simple_page.route('/modifystudent/'）
def modify_student():
    #先查出来再修改--单条
    student = Person().query.first()    
    student.s_name = "小明滚出去"     
    db.session.add(student)
    db.session.commit()
    #删除数据
    student = Person().query.first()
    db.session.delete(student)
    db.session.commit()
                   
@simple_page.route('/getpersons')
def getper():
    persons = Person().query.all()
    for person in persons:
        print(person.p_name)

    return 'GET sunceess'
