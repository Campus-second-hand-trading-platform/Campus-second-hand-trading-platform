import datetime
import json
import time

import pymysql
from flask_cors import CORS
from flask import Flask, request, Blueprint

zkh = Blueprint('zkh', __name__)
CORS(zkh, supports_credentials=True)

conn = pymysql.connect(host='localhost', port=3306, user='root', password='123456')
conn.select_db('ershou')
cursor = conn.cursor()


@zkh.route('/manager/login', methods=['POST'])
def Login():
    data = request.get_json(silent=True)
    managerid = data['mid']
    mpwd = data['mpwd']
    print(managerid)
    print(mpwd)
    search = "select * from manager where managerid='{}' and mpwd='{}'".format(managerid, mpwd)
    cursor.execute(search)
    conn.commit()
    manager = cursor.fetchone()

    msg = {
        'data': "登录成功",
        'message': "成功",
        'stateCode': 200
    }
    if manager is not None:
        return msg
    return {
        'data': "登录失败",
        'message': "失败",
        'stateCode': 202
    }


@zkh.route('/user/information', methods=['GET'])
def Userinfo():
    uid = request.args.get("userId")
    search = "select * from users where uid='{}'".format(uid)
    cursor.execute(search)
    conn.commit()
    Userinfo = cursor.fetchone()
    tmp = {
        'userId': Userinfo[0],
        'realname': Userinfo[2],
        'username': Userinfo[3],
        'department': Userinfo[4],
        'signature': Userinfo[5],
        'userPhone': Userinfo[6]
    }
    msg = {
        'message': "成功",
        'stateCode': 200,
        'data': tmp
    }
    if Userinfo is not None:
        return msg
    return {
        'data': "查无此人",
        'message': "失败",
        'stateCode': 202
    }

#买家收货确认 --todo---加判断逻辑
@zkh.route('/order/deliveryConfirmation', methods=['PUT'])
def DeliveryConfirm():
    data = request.get_json(silent=True)
    buyerid = data['userId']
    orderid = data['orderId']
    update = "update orders t set t.confirm = '1' where t.orderid = " + str(orderid) + " and t.buyerid = " + str(
        buyerid) + ";"
    cursor.execute(update)
    conn.commit()

    msg = {
        'message': "成功",
        'stateCode': 200,
        'data': "确认收货成功"
    }
    return msg


@zkh.route('/seek', methods=['GET'])
def Seek():
    uid = request.args.get("userId")
    search = "select * from seek where uid='{}'".format(uid)
    cursor.execute(search)
    conn.commit()
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


@zkh.route('/goods/<goodsId>', methods=['GET'])
def goodDetail(goodsId):
    print(goodsId)
    search = "select * from goods where gid='{}'".format(goodsId)
    cursor.execute(search)
    conn.commit()
    i = cursor.fetchone()
    tmp = {
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
        'newness': i[12],
    }
    # 获得卖家昵称
    search = "select * from users where uid='{}'".format(i[2])
    cursor.execute(search)
    conn.commit()
    j = cursor.fetchone()
    tmp['sellername'] = j[3]
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

# todo
@zkh.route('/seek/<seekid>/comments', methods=['GET'])
def Getcomments(seekid):
    search = "select * from comments where seekid='{}'".format(seekid)
    print(search)
    cursor.execute(search)
    conn.commit()
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

@zkh.route('/seek/<seekid>', methods=['GET'])
def SeekById(seekid):
    search = "select * from seek where seekid='{}'".format(seekid)
    print(search)
    cursor.execute(search)
    conn.commit()
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


@zkh.route('/orders/buyer', methods=['GET'])
def GetBuyerOrder():
    buyerid = request.args.get("userId")
    # search = "select * from orders where buyerid='{}'".format(buyerid)
    search = "select o.orderid,o.gid,o.buyerid,o.order_time,o.cancel_time,o.ostate,o.issent,o.confirm,g.gname," \
             "g.gprice,g.picture,g.sellerid from orders o,goods g where buyerid='{}' and g.gid=o.gid".format(buyerid)
    print(search)
    cursor.execute(search)
    conn.commit()
    order = cursor.fetchall()
    print(order)
    tmp = []
    for i in order:
        tmp.append({
            'orderid': i[0],
            'gid': i[1],
            'buyerid': i[2],
            'order_time': i[3].strftime("%Y-%m-%d %H:%M:%S") if i[3] is not None else 0,
            'cancel_time': i[4].strftime("%Y-%m-%d %H:%M:%S") if i[4] is not None else 0,
            'ostate': i[5],
            'issent': i[6],
            'confirm': i[7],
            'goodsName':i[8],
            'price':float(i[9]),
            'picture':i[10],
            'sellerid':i[11]
        })


    msg = {
        'message': "成功",
        'stateCode': 200,
        'data': tmp
    }
    if order is not None:
        return msg
    return {
        'message': "失败",
        'stateCode': 202,
        'data': tmp
    }
