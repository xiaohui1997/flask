from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Dispatcher, ChatMemberHandler
import requests
import telegram
from flask import jsonify
from telegram import *
from telegram.ext import *
from Public.ext import db


# 全局bot变量
bots_obj = None #context 一比一复制
bots = None
chat_id = None

#token变量
start_token = '7118659013:AAHhmIKDylUSVaDP6myn2cR6uFEfGLZ3Prw'


# 创建 Telegram 机器人处理器
def start(update: Update, context) -> None:
    '''
    :ps 每次重启或者启动需要在群里 /start一下激活变量
    :param update:
    :param context:
    :return:
    '''
    global bots
    global chat_id
    global bots_obj
    # 获取当前运行环境的公网IP
    try:
        response = requests.get('https://api.ipify.org?format=json')
        if response.status_code == 200:
            data = response.json()
            public_ip = data['ip']
            print('当前运行环境的公网IP:', public_ip)
        else:
            print('Error:', response.status_code)
    except requests.RequestException as e:
        print('Error:', str(e))

    chat_id = update.message.chat_id
    context.bot.send_message(chat_id, text="当前运行环境的公网IP: {}\napi调用当前群chatid:  {}\n方便的话请授权bot管理员权限,否则它无法主动读取群内消息!".format(str(public_ip), chat_id))
    bots = context.bot
    bots_obj = context


def help(update: Update, context) -> None:
    '''
    /help 帮助命令说明
    '''
    chat_id = update.message.chat_id
    msg = '''
    以下是帮助文档:

/start-启动机器人

可用命令如下:
/apiinfomation - api接口(主动发消息)
/cloudmonitor - 阿里云云监控说明(webhook)
/blacklist - 永久封禁ecs所有警告,使用方法 /blacklist 123(instanceId)
/test - 测试专用
/setabouttext - change bot about info
/setuserpic - change bot profile photo
/setcommands - change the list of commands
/deletebot - delete a bot

ps:请授权bot管理员权限,否则它无法主动读取群内消息!
    '''
    context.bot.send_message(chat_id,
        text=msg
    )
    
    
#临时测试使用
def test(update: Update, context) -> None:
    '''
    /help 帮助命令说明
    '''
    keyboard = [
        [InlineKeyboardButton("Button 1", callback_data='1')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)

    #reply_markup = ReplyKeyboardRemove()
    context.bot.send_message(chat_id=update.effective_chat.id,text="I'm a bot, please talk to me!",
                            reply_markup=reply_markup)

def button(update, context):
    query = update.callback_query
    query.answer()
    #处理屏蔽数据
    print(query.data)
    print("SELECT * FROM ali_webhook WHERE transId='{}'".format(str(query.data)))
    db_ali = db("SELECT * FROM ali_webhook WHERE transId='{}'".format(str(query.data)))
    if len(db_ali):
        #写入白名单
        db_ali = db_ali[0]
        res = db("INSERT INTO ali_webhook_white (rules, instanceId, isall) VALUES (?, ?, ?)", (db_ali[1], db_ali[2], 0))
        if len(res) != 0:
            msg = context.bot.send_message(chat_id, text="程序异常,请联系管理员!")
            def callback(context):
                context.bot.delete_message(chat_id=query.message.chat_id,message_id=msg.message_id)
            context.job_queue.run_once(callback, when=10)  # 10秒后运行
        else:
            msg = query.edit_message_text(text="永久屏蔽成功!")
            def callback(context):
                context.bot.delete_message(chat_id=query.message.chat_id,message_id=msg.message_id)
            context.job_queue.run_once(callback, when=10)
    else:
        msg = context.bot.send_message(chat_id, text="程序异常,请联系管理员!")
        def callback(context):
            context.bot.delete_message(chat_id=query.message.chat_id,message_id=msg.message_id)
        context.job_queue.run_once(callback, when=10)  # 10秒后运行



def apiinfomation(update: Update, context) -> None:
    '''
        /apiinfomation api主动发送消息接口说明
    '''
    chat_id = update.message.chat_id
    msg = '''
        <b>示例代码如下: </b>
        <pre>import requests

url = 'http://127.0.0.1:8833/sendmsg'
data = {
    'token': '37aba484c6261fe79d9729d93a7084c4', #自定义token 用于校验非法请求
    'chatid': '-4241574382', #群组id
    #'parse_type': 'MARKDOWN', #可选参数   类型:MARKDOWN/HTML，默认为HTML
    'msg': """<b>标题</b>  #消息内容

测试数据1
测试数据2
默认支持html
    """
}
res = requests.post(url=url, data=data)
print(res.json())
        </pre>
        '''
    context.bot.send_message(chat_id, text=msg, parse_mode=ParseMode.HTML)

def cloudmonitor(update: Update, context) -> None:
    '''
        /cloudmonitor webhook接口说明
    '''
    chat_id = update.message.chat_id
    msg = '''
<b>示例webhook地址如下: </b>
<pre>https://aliwebhook.22889.club/aliyun/webhook/37aba484c6261fe79d9729d93a7084c4/TB/-4246362489/-4245759043/+KhBOVqnJjswzOTE0?ask=akdak123==

37aba484c6261fe79d9729d93a7084c4: token(固定参数)
TB: 平台名称(根据平台名称进行替换)
-4241574382: 群组id(根据对应群组id进行替换),每个群都有个群组id,可以通过机器人获取
-4266575929: 历史记录群组ID
+KhBOVqnJjswzOTE0: 群组id(分享群组链接能看到)
?ask 可选参数,阿里云ak/sk使用base64编码,主要用于阿里api
</pre>
        '''
    context.bot.send_message(chat_id, text=msg, parse_mode=ParseMode.HTML)

# 主动撤销消息
def cancelmsg(msgid, chat_id=chat_id, secodes=10):
    def callback(bots_obj):
        bots_obj.bot.delete_message(chat_id=chat_id,message_id=msgid)
    bots_obj.job_queue.run_once(callback, when=secodes)  # 10秒后运行

# 主动回复消息
def reply_to_message(chat_id, message_id, text):
    res = bots_obj.bot.sendMessage(chat_id=chat_id, text=text, reply_to_message_id=message_id, disable_web_page_preview=True, parse_mode=telegram.ParseMode.HTML)
    return res

#拉黑操作
def blacklist(update, context):
    args = context.args
    if len(args) == 1:
        instanceId = args[0]
        res = db("INSERT INTO ali_webhook_white (instanceId, isall) VALUES (?, ?)", (str(instanceId), 1))
        if len(res) != 0:
            msg = update.message.reply_text(text="参数错误！！！")
            def callback(context):
                bots_obj.bot.delete_message(chat_id=chat_id,message_id=msg.message_id)
            bots_obj.job_queue.run_once(callback, when=10)  # 10秒后运行
        else:
            msg = update.message.reply_text(text="{},永久屏蔽成功".format(instanceId))
            def callback(context):
                bots_obj.bot.delete_message(chat_id=chat_id,message_id=msg.message_id)
            bots_obj.job_queue.run_once(callback, when=10)
    else:
        msg = update.message.reply_text(text="程序异常,请联系管理员!")
        def callback(context):
            bots_obj.bot.delete_message(chat_id=chat_id,message_id=msg.message_id)
        bots_obj.job_queue.run_once(callback, when=10)  # 10秒后运行


# 主动发送消息
def sedmsgs(msg, parse_mode=telegram.ParseMode.HTML, chat_id=chat_id, parse_type=0, ali_button=0, call_data=None, isFunc=0):
    '''
    :param msg: 发送的文字
    :param parse_mode: 类型: parse_mode=telegram.ParseMode.MARKDOWN   parse_mode=telegram.ParseMode.HTML
    :ali_button 是否需要按钮
    :reply_data 传递数据回调
    :isFunc 是否是函数调用
    :return:
    '''
    if parse_type:
        if parse_type == 'MARKDOWN':
            parse_mode = telegram.ParseMode.MARKDOWN
        elif parse_type == 'HTML':
            parse_mode = telegram.ParseMode.HTML
    if ali_button:
        #需要按钮
        keyboard = [
            [InlineKeyboardButton("永久屏蔽该消息", callback_data=call_data)],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        res = bots.send_message(chat_id, text = msg, parse_mode=parse_mode, disable_web_page_preview=True, reply_markup=reply_markup)
        pass
    else:
        res = bots.send_message(chat_id, text = msg, parse_mode=parse_mode, disable_web_page_preview=True)
    if isFunc:
        return res
    if res is not None:
        return jsonify({'code': 100003, 'msg': '发送成功'})
    else:
        return jsonify({'code': 100004, 'msg': '发送失败'})

#读取群消息
# 处理群组消息的函数
def handle_group_message(update: Update, context) -> None:
    # message = update.message
    # chat_id = message.chat_id
    # text = message.text
    pass

    # 在这里处理群组消息
    # 可以根据需要编写逻辑来响应不同的消息内容
    #企业id 处理--业务
    # res = qyid(text)
    # if res is not None:
    #     context.bot.send_message(chat_id=chat_id, text=f"{res[0]}")
    #     context.bot.send_message(chat_id=chat_id, text=f"{res[1]}")
    #     context.bot.send_message(chat_id=chat_id, text=f"--"*30)
    # 示例：回复收到的消息
    #context.bot.send_message(chat_id=chat_id, text=f"You said: {text}")

#bot从群里删除或者添加时触发
def chat_member_updated(update: Update, context: CallbackContext):
    print(update.message.chat_id)
    help(update, context)

def tg_main():
    # 创建 Updater 对象
    updater = Updater(token=start_token, use_context=True)

    # 获取 Dispatcher 对象
    dispatcher = updater.dispatcher

    # 添加命令处理器
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler("test", test))
    dispatcher.add_handler(CommandHandler("blacklist", blacklist))
    dispatcher.add_handler(CallbackQueryHandler(button))
    dispatcher.add_handler(CommandHandler("apiinfomation", apiinfomation))
    dispatcher.add_handler(CommandHandler("cloudmonitor", cloudmonitor))
    dispatcher.add_handler(ChatMemberHandler(chat_member_updated))
    # 添加 MessageHandler 处理器，指定处理群组消息的函数和过滤器
    group_message_handler = MessageHandler(Filters.group, handle_group_message)
    dispatcher.add_handler(group_message_handler)
    # 启动机器人轮询
    updater.start_polling()
