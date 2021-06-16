import pymysql
from flask_cors import CORS
from flask import Flask, request, Blueprint
# from hs import hs
# from zkh import zkh
# from wyb import wyb
# from yjr import yjr
from login1 import login1
from goods1 import goods1
from orders import orders
from manager import manager
from seek import seek
from pic import pic
from chat import chat

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.debug = True


def conn_db():
    # 连接数据库
    db = pymysql.Connect("localhost", "root", "123456", "ershou")
    return db


# app.register_blueprint(hs,url_prefix='/')
# app.register_blueprint(zkh,url_prefix='/')
# app.register_blueprint(wyb,url_prefix='/')
# app.register_blueprint(yjr,url_prefix='/')

app.register_blueprint(login1, url_prefix='/')
app.register_blueprint(goods1, url_prefix='/')
app.register_blueprint(orders, url_prefix='/')
app.register_blueprint(manager, url_prefix='/')
app.register_blueprint(seek, url_prefix='/')
app.register_blueprint(pic, url_prefix='/')
app.register_blueprint(chat, url_prefix='/')

if __name__ == '__main__':
    app.run(debug=True, port=9000)
