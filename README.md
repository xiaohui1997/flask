# telegram_python
python-telegram-bot.org 13.1

python3.6可顺利运行

#### 基础环境
```bash
yum install python3-devel
pip3 install -r requirements.txt -i https://mirrors.163.com/pypi/simple/
mkdir /var/log/telegram
yum install supervisor
#
将telegram.ini 移动到supervisor配置文件目录中
#重启更新
supervisorctl reread all
```