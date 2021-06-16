import datetime
import random

import pymysql
from werkzeug.utils import secure_filename
import os
from flask_cors import CORS
from flask import Flask, request, Blueprint,jsonify

chat = Blueprint('chat', __name__)
CORS(chat, supports_credentials=True)

def conn_db():
    # 连接数据库
    db = pymysql.Connect("localhost", "root", "123456", "ershou")
    return db

# 获得指定用户聊天列表
@chat.route("/chattinglist", methods=['GET'])
def getUserChatList():
    db = conn_db()  # 连接数据库
    cursor = db.cursor()  # 使用 cursor() 方法创建一个游标对象 cursor
    uid = request.args.get("userId")
    # 最近的一条聊天内容
    sql = "select chat.chatid,chat.senderid,chat.receiverid,chat.chattext,chat.chattime from chat " \
          "where chat.chattime in" \
          "(select max(chattime) from chat where senderid=%s or receiverid=%s group by chatid)"
    cursor.execute(sql, [uid, uid])
    store = cursor.fetchall()
    data = store
    print(data)
    temp = []
    for i in data:
        sid = i[1]
        rid = i[2]
        chattext = i[3]
        if sid != uid:
            userId = sid
        else:
            userId = rid
        sql1 = "select nickname from users where uid=%s"
        cursor.execute(sql1, [userId])
        nn = cursor.fetchall()
        nickname = nn[0][0]
        temp.append({
            "userId": userId,
            "nickname": nickname,
            "chattext": chattext
        })
    res = {
        "stateCode": 200,
        "message": "成功",
        "data": temp
    }
    print(temp)
    db.close()
    cursor.close()
    return res


# 获得指定用户聊天内容
@chat.route("/chatting", methods=['GET'])
def getChatContent():
    db = conn_db()  # 连接数据库
    cursor = db.cursor()  # 使用 cursor() 方法创建一个游标对象 cursor
    myid = request.args.get("userId1")  # 自己id
    otherid = request.args.get("userId2")  # 对方id
    sql1 = "select nickname from users where uid=%s"
    cursor.execute(sql1, [myid])
    data1 = cursor.fetchall()
    myname = data1[0][0]
    sql2 = "select nickname from users where uid=%s"
    cursor.execute(sql2, [otherid])
    data2 = cursor.fetchall()
    othername = data2[0][0]
    sql = "select senderid,receiverid,chattext,chattime from chat " \
          "where (senderid=%s and receiverid=%s) " \
          "or (senderid=%s and receiverid=%s) " \
          "order by chattime asc"
    cursor.execute(sql, [myid, otherid, otherid, myid])
    data = cursor.fetchall()
    temp = []
    for i in data:
        sid = i[0]
        # rid = i[1]
        chattext = i[2]
        if sid == myid:
            sname = myname
        else:
            sname = othername
        temp.append({
            "sendId": sid,
            "nickname": sname,
            "chattext": chattext
        })
    res = {
        "stateCode": 200,
        "message": "成功",
        "data": temp
    }
    print(temp)
    db.close()
    cursor.close()
    return res


# 发送聊天
@chat.route("/chatting/send", methods=['POST'])
def sendChat():
    db = conn_db()  # 连接数据库
    cursor = db.cursor()  # 使用 cursor() 方法创建一个游标对象 cursor
    data = request.get_json(silent=True)
    myId = data["userId1"]  # 自己id
    otherId = data["userId2"]  # 对方id
    chattext = data['chattext'] # 发送内容
    chattime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 发送时间
    if myId < otherId:
        chatid = myId + otherId
    else:
        chatid = otherId + myId
    sql = "insert into chat(chatid,senderid,receiverid,chattext,chattime)values(%s,%s,%s,%s,%s)"
    cursor.execute(sql, [chatid, myId, otherId, chattext,chattime])
    db.commit()
    res = {
        "stateCode": "200",
        "message": "成功",
        "data": "成功"
    }
    db.close()
    cursor.close()
    return res


