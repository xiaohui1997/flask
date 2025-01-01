from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def index():
    # 获取 User-Agent 请求头
    user_agent = request.headers.get('name')
    print(request.headers)
    return f'你的name请求头为{user_agent}'

if __name__ == '__main__':
    app.run(host="0.0.0.0")