import datetime
import json
import time

import pymysql
from flask_cors import CORS
from flask import Flask, request, Blueprint

wyb = Blueprint('wyb', __name__)
CORS(wyb, supports_credentials=True)

conn = pymysql.connect(host='localhost', port=3306, user='root', password='123456')
conn.select_db('ershou')
cursor = conn.cursor()


def conn_db():
    # 连接数据库
    db = pymysql.Connect("localhost", "root", "123456", "ershou")
    return db
# 获取指定订单---todo
@wyb.route('/orders/<orderid>', methods = ['GET'])
def getOrder(orderid):
    db = conn_db()  # 连接数据库
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    print(orderid)
    create1 = "select * from orders o,goods g where o.gid=g.gid and o.orderid = '" + orderid + "';"
    print(create1)
    cursor.execute(create1)
    conn.commit()
    i = cursor.fetchone()
    print(i)
    tmp = {
            'orderid': i[0],
            'gid': i[1],
            'buyerid': i[2],
            'order_time': i[3].strftime("%Y-%m-%d %H:%M:%S") if i[3] is not None else 0,
            'cancel_time': i[4].strftime("%Y-%m-%d %H:%M:%S") if i[4] is not None else 0,
            'ostate': i[5],
            'issent': i[6],
            'confirm': i[7],
            'gname':i[10],
            'price':float(i[12])

        }

    msg = {
       'data': tmp,
        'message': "成功",
        'stateCode': 200
    }
    return msg



###发布求购###
###################
@wyb.route('/seek', methods = ['POST'])
def PostSeek():

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
    conn.commit()
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
@wyb.route('/seek/<seekId>', methods = ['DELETE'])
def DeleteSeek(seekId):
    print(seekId)
    create1 = "delete from seek where seekid = '" + seekId + "';"
    print(create1)
    cursor.execute(create1)
    conn.commit()

    msg = {
        'data': "删除成功",
        'message': "成功",
        'stateCode': 200
    }
    return msg


##用户举报指定商品###
##################
@wyb.route('/report', methods = ['POST'])
def PostReport():

    # 获取前端数据
    data = request.get_json(silent=True)
    gid = data['goodsid']
    uid = data['userId']
    rreason = data['reason']
    timenowstr = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    # 自增reportid
    reportid = 0
    getnum = "select reportid from report"
    cursor.execute(getnum)
    data4 = cursor.fetchall()
    for i in data4:
        print(i[0])
        if int(i[0]) > reportid:
            reportid = int(i[0])

    reportid = reportid + 1

    print(reportid)



    create1 = "INSERT INTO report (reportid,uid,gid,rtime,rreason,rstate) values ("+ str(reportid) + "," + str(uid) + "," + str(gid) + ",'" + timenowstr + "','" + rreason + "','" + "0" + "');"
    print(create1)
    cursor.execute(create1)
    conn.commit()

    msg = {
        'data': "举报成功",
        'message': "成功",
        'stateCode': 200
    }
    return msg



##搜索获得商品##
@wyb.route('/goods/search', methods = ['GET'])
def searchGoods():
    db = conn_db()  # 连接数据库
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    searchKey = request.args.get("searchKey")
    print(searchKey)
    create1 = "select * from goods where gname like '%"+ searchKey +"%';"
    print(create1)
    cursor.execute(create1)
    conn.commit()
    data = cursor.fetchall()
    tmp = []
    for i in data:
        tmp.append({
            'gid': i[0],
            'gname': i[1],
            'sellerid': i[2],
            'gprice': float(i[3]),
            'gtype': i[4],
            'gstate': i[5],
            'gcount': i[6],
            'gdescription': i[7],
            'upload_time':i[8],
            'remove_time':i[9],
            'picture':i[10],
            'morepic':i[11],
            'newness':i[12]

        })
    msg = {
       'data': tmp,
        'message': "成功",
        'stateCode': 200
    }
    return msg

# 获取所有求购
@wyb.route('/seeks', methods = ['GET'])
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
@wyb.route('/seek/<seekid>/comments', methods=['GET'])
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

##获取指定用户的所有订单
###################
@wyb.route('/orders/seller', methods = ['GET'])
def getAllSale():
    db = conn_db()  # 连接数据库
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    userid = request.args.get("userId")
    create1 = "select o.orderid,o.gid,o.buyerid,o.order_time,o.cancel_time,o.ostate,o.issent,o.confirm,g.picture,u.uname,g.gname,g.gprice from goods g, orders o, users u " \
              "where g.sellerid = '" + userid + "' and o.ostate = 1 and o.buyerid = u.uid and g.gid=o.gid;"
    create2 = "select users.uname from users where users.uid = '" + userid + "';"
    print(create1)
    cursor.execute(create1)
    data = cursor.fetchall()
    le = len(data)
    print(data)
    tmp = []
    for i in data:
        print(i[6])
        tmp.append({
            'orderid': i[0],
            'gid': i[1],
            'buyerid': i[2],
            'order_time': i[3].strftime("%Y-%m-%d %H:%M:%S") if i[3] is not None else 0,
            'cancel_time':i[4].strftime("%Y-%m-%d %H:%M:%S") if i[4] is not None else 0,
            'state': i[5],
            'issent': i[6],
            'confirm': i[7],
            'picture': i[8],
            'buyername': i[9],
            'goodsName': i[10],
            'price': float(i[11])
        })
        cursor.execute(create2)
        j = cursor.fetchone()
        for i in range(0, le):
            tmp[i]["sellername"] = j[0]



    msg = {
        'message': "成功",
        'stateCode': 200,
        'data': tmp
    }
    cursor.close()
    db.close()
    return msg