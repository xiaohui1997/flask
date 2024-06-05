from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Dispatcher, ChatMemberHandler
import requests
import telegram
from flask import jsonify
from telegram import *
from telegram.ext import *



# 全局bot变量
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
    chat_id = update.message.chat_id

    menu_buttons = [
        ['Create Bot', 'My Bots'],  # 这两个命令是 BotFather 菜单上的命令，你可以根据你的需求进行替换
        ['Edit Bot', 'Bot Settings'],
    ]
    reply_markup = ReplyKeyboardRemove()
    context.bot.send_message(chat_id=update.effective_chat.id, text="You chose: " + update.message.text,
                            reply_markup=reply_markup)


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

# 主动发送消息
def sedmsgs(msg, parse_mode=telegram.ParseMode.HTML, chat_id=chat_id, parse_type=0):
    '''
    :param msg: 发送的文字
    :param parse_mode: 类型: parse_mode=telegram.ParseMode.MARKDOWN   parse_mode=telegram.ParseMode.HTML
    :return:
    '''
    if parse_type:
        if parse_type == 'MARKDOWN':
            parse_mode = telegram.ParseMode.MARKDOWN
        elif parse_type == 'HTML':
            parse_mode = telegram.ParseMode.HTML
    res = bots.send_message(chat_id, text = msg, parse_mode=parse_mode)
    if res is not None:
        return jsonify({'code': 100003, 'msg': '发送成功'})
    else:
        return jsonify({'code': 100004, 'msg': '发送失败'})

#读取群消息
# 处理群组消息的函数
def handle_group_message(update: Update, context) -> None:
    message = update.message
    chat_id = message.chat_id
    text = message.text

    # 在这里处理群组消息
    # 可以根据需要编写逻辑来响应不同的消息内容
    #企业id 处理--业务
    # res = qyid(text)
    # if res is not None:
    #     context.bot.send_message(chat_id=chat_id, text=f"{res[0]}")
    #     context.bot.send_message(chat_id=chat_id, text=f"{res[1]}")
    #     context.bot.send_message(chat_id=chat_id, text=f"--"*30)
    # 示例：回复收到的消息
    context.bot.send_message(chat_id=chat_id, text=f"You said: {text}")

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
    dispatcher.add_handler(CommandHandler("apiinfomation", apiinfomation))
    dispatcher.add_handler(ChatMemberHandler(chat_member_updated))
    # 添加 MessageHandler 处理器，指定处理群组消息的函数和过滤器
    group_message_handler = MessageHandler(Filters.group, handle_group_message)
    dispatcher.add_handler(group_message_handler)
    # 启动机器人轮询
    updater.start_polling()