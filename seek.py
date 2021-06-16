import datetime
import json
import time
from datetime import timedelta, date
import pymysql
from flask_cors import CORS
from flask import Flask, render_template, request, jsonify, Blueprint
from random import Random
from config import conn_db

seek = Blueprint('seek', __name__)
CORS(seek, supports_credentials=True)

#获得指定用户的所有求购
@seek.route('/seek', methods=['GET'])
def Seek():
    db = conn_db()  # 连接数据库
    cursor = db.cursor()  # 使用 cursor() 方法创建一个游标对象 cursor
    uid = request.args.get("userId")
    search = "select * from seek where uid='{}'".format(uid)
    cursor.execute(search)
    db.commit()
    seek = cursor.fetchall()
    tmp = []
    for i in seek:
        tmp.append({
            'seekid': i[0],
            'stitle': i[2],
            'sdescription': i[3],
            'stime': i[4].strftime("%Y-%m-%d %H:%M:%S") if i[4] is not None else 0
        })

    msg = {
        'message': "成功",
        'stateCode': 200,
        'data': tmp
    }
    if seek is not None:
        return msg
    return {
        'message': "失败",
        'stateCode': 202,
        'data': tmp
    }


# 修改我的求购
@seek.route("/seek/<id>", methods=['PUT'])
def ModifyMySeek(id):
    db = conn_db()  # 连接数据库
    cursor = db.cursor()  # 使用 cursor() 方法创建一个游标对象 cursor
    uid = request.json.get("userId")
    title = request.json.get("stitle")
    desc = request.json.get("sdescription")
    # type = request.json.get("type")
    sql = "select * from seek where seekid=%s and uid=%s"
    print(id)
    print(uid)
    ret = cursor.execute(sql, [id, uid])
    if ret > 0:
        # sql1 = "update seek set stitle=%s,sdescription=%s,stype=%s where seekid=%s"
        sql1 = "update seek set stitle=%s,sdescription=%s where seekid=%s"
        cursor.execute(sql1, [title, desc, id])
        db.commit()
        res = {
            "stateCode": 200,
            "message": "成功",
            "data": "修改成功"
        }
    else:
        res = {
            "stateCode": 202,
            "message": "失败",
            "data": "信息匹配错误"
        }
    db.close()
    cursor.close()
    return res

###发布求购###
###################
@seek.route('/seek', methods = ['POST'])
def PostSeek():
    db = conn_db()  # 连接数据库
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # 获取前端数据
    data = request.get_json(silent=True)
    userId = data['userId']
    stitle = data['stitle']
    sdescription = data['sdescription']
    type = data['type']
    timenowstr = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    create1 = "INSERT INTO seek (seekid,uid,stitle,sdescription,stime) values ('" + userId + timenowstr + "','" + userId + "','" + stitle + "','" + sdescription + "','" + timenowstr + "');"
    show = "select * from seek where seekid = '" + userId + timenowstr + "';"
    print(create1)
    cursor.execute(create1)
    cursor.execute(show)
    db.commit()
    data = cursor.fetchall()
    tmp = []
    for i in data:
        tmp.append({
            'seekid': i[0],
            'uid': i[1],
            'stitle': i[2],
            'sdescription': i[3],
            'stime': i[4],

        })
    msg = {
        'data': tmp,
        'message': "成功",
        'stateCode': 200
    }
    return msg



###删除求购信息###
###################
@seek.route('/seek/<seekId>', methods = ['DELETE'])
def DeleteSeek(seekId):
    db = conn_db()  # 连接数据库
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    print(seekId)
    create1 = "delete from seek where seekid = '" + seekId + "';"
    print(create1)
    cursor.execute(create1)
    db.commit()

    msg = {
        'data': "删除成功",
        'message': "成功",
        'stateCode': 200
    }
    return msg

# 获取指定求购评论todo
@seek.route('/seek/<seekid>/comments', methods=['GET'])
def Getcomments(seekid):
    db = conn_db()  # 连接数据库
    cursor = db.cursor()  # 使用 cursor() 方法创建一个游标对象 cursor
    search = "select * from comments where seekid='{}'".format(seekid)
    print(search)
    cursor.execute(search)
    db.commit()
    comment = cursor.fetchall()
    tmp = []
    for i in comment:
        tmp.append({
            'commentid': i[0],
            'seekid': i[1],
            'uid': i[2],
            'commenttime': i[3].strftime("%Y-%m-%d %H:%M:%S") if i[4] is not None else 0,
            'commentcontent': i[4],
        })

    msg = {
        'message': "成功",
        'stateCode': 200,
        'data': tmp
    }
    if comment is not None:
        return msg
    return {
        'message': "失败",
        'stateCode': 202,
        'data': tmp
    }
#获取指定求购信息
@seek.route('/seek/<seekid>', methods=['GET'])
def SeekById(seekid):
    db = conn_db()  # 连接数据库
    cursor = db.cursor()  # 使用 cursor() 方法创建一个游标对象 cursor
    search = "select * from seek where seekid='{}'".format(seekid)
    print(search)
    cursor.execute(search)
    db.commit()
    i = cursor.fetchone()
    tmp = {
            'seekid': i[0],
            'userId': i[1],
            'stitle': i[2],
            'sdescription': i[3],
            'stime': i[4].strftime("%Y-%m-%d %H:%M:%S") if i[4] is not None else 0
        }

    msg = {
        'message': "成功",
        'stateCode': 200,
        'data': tmp
    }
    if i is not None:
        return msg
    return {
        'message': "失败",
        'stateCode': 202,
        'data': tmp
    }

# 评论求购
@seek.route("/seek/comment", methods=['POST'])
def comment():
    db = conn_db()  # 连接数据库
    cursor = db.cursor()  # 使用 cursor() 方法创建一个游标对象 cursor
    data = request.get_json(silent=True)
    # seekId
    # userId
    # content
    seekId = data['seekId']  # 求购id
    uid = data['userId']  # 评论人id
    content = data['content']  # 评论内容
    comment_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 评论时间
    sql = "insert into comments(seekid,uid,commenttime,commentcontent)values(%s,%s,%s,%s)"
    cursor.execute(sql, [seekId, uid, comment_time, content])
    db.commit()
    sql1 = "select commentid,seekid,uid,commenttime,commentcontent from comments where seekid=%s"
    cursor.execute(sql1, [seekId])
    data1 = cursor.fetchall()
    # print(data1)
    temp = []
    for i in data1:
        temp.append({
            'commentId': i[0],
            'seekId': i[1],
            'userId': i[2],
            'comment_time': i[3],
            'content': i[4]
        })
    # print(temp)
    res = {
        "stateCode": 200,
        "message": "成功",
        "data": temp
    }
    db.close()
    cursor.close()
    return res

# 获取所有求购
@seek.route('/seeks', methods = ['GET'])
def getAllseek():
    db = conn_db()  # 连接数据库
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    create1 = "select * from seek;"
    cursor.execute(create1)
    data = cursor.fetchall()
    tmp = []
    for i in data:
        tmp.append({
            'seekid': i[0],
            'uid': i[1],
            'stitle': i[2],
            'sdescription': i[3],
            'stime': i[4].strftime("%Y-%m-%d %H:%M:%S") if i[4] is not None else 0
        })
    msg = {
        'message': "成功",
        'stateCode': 200,
        'data': tmp
    }
    return msg

#获取指定求购评论
@seek.route('/seek/<seekid>/comments', methods=['GET'])
def getAllcomments(seekid):
    db = conn_db()  # 连接数据库
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    search = "select * from comments where seekid = '{}'".format(seekid)
    cursor.execute(search)
    data = cursor.fetchall()
    tmp = []
    for i in data:
        tmp.append({
            'commentid': i[0],
            'seekid': i[1],
            'uid': i[2],
            'commenttime': i[3].strftime("%Y-%m-%d %H:%M:%S") if i[3] is not None else 0,
            'commentcontent': i[4]
        })
    msg = {
        'message': "成功",
        'stateCode': 200,
        'data': tmp
    }
    return msg