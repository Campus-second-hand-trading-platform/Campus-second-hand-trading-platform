import datetime
import json
import time

import pymysql
from flask_cors import CORS
from flask import Flask, request, Blueprint

hs = Blueprint('hs', __name__)
CORS(hs, supports_credentials=True)

conn = pymysql.connect(host='localhost', port=3306, user='root', password='123456')
conn.select_db('ershou')
cursor = conn.cursor()

def conn_db():
    # 连接数据库
    db = pymysql.Connect("localhost", "root", "123456", "ershou")
    return db
# 生成指定货物的订单--done
@hs.route('/orders', methods=['POST'])
def OrderCreate():
    # 获取前端数据
    data = request.get_json(silent=True)
    gid = data['gid']
    buyerid = data['buyerid']
    print(gid)
    print(buyerid)
    timenowstr = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    create1 = "INSERT INTO orders (orderid,gid,buyerid,order_time,ostate) values (" + str(buyerid) + str(
        gid) + timenowstr + "," + str(gid) + "," + str(buyerid) + ",'" + timenowstr + "','" + '0' + "');"
    show1 = "select orderid,o.gid,buyerid,order_time,cancel_time,ostate,issent,confirm,sent_time,gname,uname from orders o,goods g,users u where o.orderid = '" + str(buyerid) + str(gid) + timenowstr + "' and o.gid = " + str(
        gid) + " and g.gid = " + str(gid) + " and o.gid = g.gid and o.buyerid = '" + str(buyerid) + "' and u.uid = '" + str(buyerid) +"' and o.buyerid = u.uid;"
    show2 = "select uname from goods g,users u where g.gid = " + str(gid) + " and g.sellerid = u.uid;"
    print(create1)
    print(show1)
    cursor.execute(create1)
    cursor.execute(show1)
    conn.commit()
    i = cursor.fetchone()
    print(i)
    tmp = {
        'orderid': i[0],
        'gid': i[1],
        'buyerid': i[2],
        'order_time': i[3].strftime("%Y-%m-%d %H:%M:%S"),
        'cancel_time': i[4].strftime("%Y-%m-%d %H:%M:%S") if i[4] is not None else 0,
        'ostate': i[5],
        'issent': i[6],
        'confirm': i[7],
        'sent_time': i[8],
        'gname': i[9],
        'buyerName': i[10]
    }
    cursor.execute(show2)
    j = cursor.fetchone()
    print(j)
    tmp['sellerName'] = j[0]
    msg = {
        'stateCode': 200,
        'message': "成功",
        'data': tmp
    }
    if j[0] == i[10] :
        msg2 = {
            'stateCode': 202,
            'message': "失败"
        }
        return msg2
    else :
        return msg





# 订单购买--done---没做检测，商品是否已被买走
@hs.route('/orders/buy', methods=['PUT'])
def buy():
    # 获取前端数据
    data = request.get_json(silent=True)
    orderid = data['orderid']
    buyerid = data['buyerid']

    judge = "select * from goods g,orders o where orderid ='{}' and o.gid = g.gid and g.gstate = 1;".format(orderid)
    cursor.execute(judge)
    print(judge)
    result = cursor.fetchone()
    print(result)
    if result is not None:
        update1 = "update orders t set t.ostate = '1' where t.orderid = '" + str(orderid) + "' and t.buyerid = '" + str(
        buyerid) + "';"
        update2 = "update goods g,orders o set g.gstate = '0' where o.orderid = '" + str(
        orderid) + "' and o.buyerid = '" + str(buyerid) + "' and o.gid = g.gid;"
        print(update1)
        print(update2)
        cursor.execute(update1)
        cursor.execute(update2)
        conn.commit()

        msg = {
            'stateCode': 200,
            'message': "成功",
            'data': "购买成功"
        }
        return msg
    else:
        msg2 = {
            'stateCode': 202,
            'message': "失败",
            'data': "商品已被买走"
        }
        return msg2


# #获得某一类型的所有商品--done
@hs.route('/goods', methods=['GET'])
def goods():
    db = conn_db()  # 连接数据库
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # 获取前端数据
    gtype =  request.args.get("type")
    print(gtype)
    show = "select * from goods where gtype = " + str(gtype) + " and gstate = 1 and gcount = 1;"
    print(show)
    cursor.execute(show)
    data = cursor.fetchall()
    print(data)
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
            'upload_time': i[8].strftime("%Y-%m-%d %H:%M:%S") if i[8] is not None else 0,
            'remove_time': i[9].strftime("%Y-%m-%d %H:%M:%S") if i[9] is not None else 0,
            'picture': i[10],
            'morepic': i[11],
            'newness': i[12]

        })
    msg = {
        'stateCode': 200,
        'message': "成功",
        'data': tmp
    }
    return msg


# 卖家发布商品--done
@hs.route('/goods', methods=['POST'])
def goodsSeller():
    # 获取前端数据
    data = request.get_json(silent=True)
    gname = data['gname']
    sellerid = data['sellerid']
    gprice = data['gprice']
    gtype = data['gtype']
    gcount = 1
    gdescription = data['gdescription']
    picture = data['picture']
    newness = data['newness']
    gstate = 1

    print(gname)
    print(sellerid)
    print(gprice)
    print(gtype)

    timenowstr = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    # 自增gid
    gid = 0
    getnum = "select gid from goods"
    cursor.execute(getnum)
    data4 = cursor.fetchall()
    for i in data4:
        print(i[0])
        if int(i[0]) > gid:
            gid = int(i[0])

    gid = gid + 1

    print(gid)

    publish = "INSERT INTO goods (gid,gname,sellerid,gprice,gtype,gstate,gcount,gdescription,upload_time,picture,newness) values (" + str(
        gid) + ",'" + str(gname) + "','" + str(sellerid) + "'," + str(gprice) + "," + str(gtype) + "," + str(
        gstate) + "," + str(gcount) + ",'" + str(gdescription) + "','" + timenowstr + "','" + str(picture) + "'," + str(
        newness) + ");"
    print(publish)
    cursor.execute(publish)
    conn.commit()

    msg = {
        'stateCode': 200,
        'message': "成功",
        'data': "上架商品成功"
    }
    return msg


# 管理员获得所有举报信息--done
@hs.route('/reports', methods=['GET'])
def reports():
    db = conn_db()  # 连接数据库
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # 获取前端数据

    show = "select * from report;"
    cursor.execute(show)
    data = cursor.fetchall()
    print(data)
    tmp = []
    for i in data:
        tmp.append({
            'reportid': i[0],
            'uid': i[1],
            'gid': i[2],
            'managerid': i[3],
            'rtime': i[4].strftime("%Y-%m-%d %H:%M:%S") if i[4] is not None else 0,
            'rreason': i[5],
            'rstate': i[6]
        })
    msg = {
        'stateCode': 200,
        'message': "成功",
        'data': tmp
    }
    return msg

# 管理员获得所有举报信息
@hs.route('/reports/unsolved', methods = ['GET'])
def reports2():
    db = conn_db()  # 连接数据库
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # 获取前端数据

    show = "select * from report where rstate = 0;"
    print(show)
    cursor.execute(show)
    data = cursor.fetchall()
    print(data)
    tmp = []
    for i in data:
        tmp.append({
            'reportid': i[0],
            'uid': i[1],
            'gid': i[2],
            'managerid': i[3],
            'rtime': i[4].strftime("%Y-%m-%d %H:%M:%S") if i[4] is not None else 0,
            'rreason': i[5],
            'rstate': i[6]
        })
    msg = {
        'stateCode': 200,
        'message': "成功",
        'data': tmp
    }
    return msg

# 卖家获得我的商品信息
@hs.route('/seller/goods', methods = ['GET'])
def sellergoods():
    # 获取前端数据
    uid = request.args.get('userId')
    print(uid)
    show = "select * from goods where sellerid = '" + str(uid) + "' ;"
    print(show)
    cursor.execute(show)
    data = cursor.fetchall()
    print(data)
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
            'upload_time': i[8].strftime("%Y-%m-%d %H:%M:%S") if i[8] is not None else 0,
            'remove_time': i[9].strftime("%Y-%m-%d %H:%M:%S") if i[9] is not None else 0,
            'picture': i[10],
            'morepic': i[11],
            'newness': i[12]

        })
    msg = {
        'stateCode': 200,
        'massage': "成功",
        'data': tmp
    }
    return msg
