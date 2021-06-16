import datetime
import json
import time
from datetime import timedelta, date
import pymysql
from flask_cors import CORS
from flask import Flask, render_template, request, jsonify, Blueprint
from random import Random
from config import conn_db

orders = Blueprint('orders', __name__)
CORS(orders, supports_credentials=True)


# 生成指定货物的订单--done
@orders.route('/orders', methods=['POST'])
def OrderCreate():
    db = conn_db()  # 连接数据库
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
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
    db.commit()
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


# 获取指定订单---todo
@orders.route('/orders/<orderid>', methods = ['GET'])
def getOrder(orderid):
    db = conn_db()  # 连接数据库
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    print(orderid)
    create1 = "select * from orders o,goods g where o.gid=g.gid and o.orderid = '" + orderid + "';"
    print(create1)
    cursor.execute(create1)
    db.commit()
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

##获取指定用户的所有订单
###################
@orders.route('/orders/seller', methods = ['GET'])
def getAllSale():
    db = conn_db()  # 连接数据库
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    userid = request.args.get("userId")
    create1 = "select o.orderid,o.gid,o.buyerid,o.order_time,o.cancel_time,o.ostate,o.issent,o.confirm,g.picture,u.uname,g.gname,g.gprice from goods g, orders o, users u " \
              "where g.sellerid = '" + userid + "' and o.ostate = 1 and o.buyerid = u.uid and g.gid=o.gid;"
    create2 = "select users.uname from users where users.uid = '" + userid + "';"
    cursor.execute(create1)
    data = cursor.fetchall()
    le = len(data)
    print(data)
    tmp = []
    for i in data:
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

@orders.route('/orders/buyer', methods=['GET'])
def GetBuyerOrder():
    db = conn_db()  # 连接数据库
    cursor = db.cursor()  # 使用 cursor() 方法创建一个游标对象 cursor
    buyerid = request.args.get("userId")
    # search = "select * from orders where buyerid='{}'".format(buyerid)
    search = "select o.orderid,o.gid,o.buyerid,o.order_time,o.cancel_time,o.ostate,o.issent,o.confirm,g.gname," \
             "g.gprice,g.picture,g.sellerid from orders o,goods g where buyerid='{}' and g.gid=o.gid".format(buyerid)
    print(search)
    cursor.execute(search)
    db.commit()
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


#买家收货确认 --todo---加判断逻辑
@orders.route('/order/deliveryConfirmation', methods=['PUT'])
def DeliveryConfirm():
    db = conn_db()  # 连接数据库
    cursor = db.cursor()  # 使用 cursor() 方法创建一个游标对象 cursor
    data = request.get_json(silent=True)
    buyerid = data['userId']
    orderid = data['orderId']
    update = "update orders t set t.confirm = '1' where t.orderid = " + str(orderid) + " and t.buyerid = " + str(
        buyerid) + ";"
    cursor.execute(update)
    db.commit()

    msg = {
        'message': "成功",
        'stateCode': 200,
        'data': "确认收货成功"
    }
    return msg

# 订单购买--done---没做检测，商品是否已被买走
@orders.route('/orders/buy', methods=['PUT'])
def buy():
    db = conn_db()  # 连接数据库
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
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
        db.commit()

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

# 买家取消订单支付-删除
@orders.route("/order/cancel", methods=['PUT'])
def cancelOrder():
    db = conn_db()  # 连接数据库
    cursor = db.cursor()  # 使用 cursor() 方法创建一个游标对象 cursor
    oid = request.json.get("orderId")
    uid = request.json.get("userId")
    sql = "select * from orders where orderid=%s and buyerid=%s"
    ret = cursor.execute(sql, [oid, uid])
    if ret > 0:  # 信息匹配正确
        sql2 = "select issent from orders where orderid=%s and buyerid=%s"
        cursor.execute(sql2, [oid, uid])
        data = cursor.fetchall()
        issent = data[0][0]
        if issent == 1:  # 未发货，可以取消
            sql1 = "delete from orders where orderid=%s"  # 0支付失败,1支付成功,2支付成功后退款，取消支付并不记录cancel时间
            cursor.execute(sql1, [oid])
            db.commit()
            res = {
                "stateCode": 200,
                "message": "成功",
                "data": "取消订单成功"
            }
        else:  # 已经发货，不能取消
            res = {
                "stateCode": "202",
                "message": "失败",
                "data": "已经发货,取消订单成功"
            }
    else:
        res = {
            "stateCode": "202",
            "message": "失败",
            "data": "信息匹配错误"
        }
    db.close()
    cursor.close()
    return res


# 买家退款--todo
@orders.route("/order/drawback", methods=['GET'])
def drawback():
    db = conn_db()  # 连接数据库
    cursor = db.cursor()  # 使用 cursor() 方法创建一个游标对象 cursor
    oid = request.args.get("orderId")
    cancel_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # 判断商品是否已经确认发货了
    sql = "select goods.gid,issent from goods,orders where goods.gid=orders.gid and orderid=%s"
    cursor.execute(sql, [oid])
    data = cursor.fetchall()
    gid = data[0][0]
    issent = data[0][1]
    if issent == 1:  # 未发货
        sql1 = "update orders set ostate=%s,cancel_time=%s where orderid=%s"  # 0支付失败,1支付成功,2支付成功后退款,退款后记录退款时间
        cursor.execute(sql1, [2, cancel_time, oid])
        sql2 = "update goods set gstate=%s where gid=%s"
        cursor.execute(sql2, [1, gid])
        db.commit()
        res = {
            "stateCode": 200,
            "message": "成功",
            "data": "退款成功"
        }
    else:  # 已经发货了
        res = {
            "stateCode": 202,
            "message": "失败",
            "data": "卖家已经发货，不能退款"
        }
    db.close()
    cursor.close()
    return res

# 卖家确认订单发货接口
@orders.route("/order/beginDelivery", methods=['PUT'])
def confirmSent():
    db = conn_db()  # 连接数据库
    cursor = db.cursor()  # 使用 cursor() 方法创建一个游标对象 cursor
    userId = request.json.get("userId")
    orderId = request.json.get("orderId")
    sql2 = "select * from orders,goods where orders.gid=goods.gid and orders.orderid=%s and goods.sellerid=%s"
    ret = cursor.execute(sql2, [orderId, userId])  # 验证权限
    if ret > 0:
        sql = "select ostate,issent from orders where orderid=%s"
        cursor.execute(sql, [orderId])
        data = cursor.fetchone()
        sent = data[1]  # 看是否发货了，1未发货,0已发货
        state = data[0]  # 看是否成功购买了，0支付失败,1支付成功,2支付成功后退款
        if state == 1:
            if sent == 1:
                print(123)
                sent_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                sql1 = "update orders set issent=%s,sent_time=%s where orderid=%s"
                cursor.execute(sql1, [0, sent_time, orderId])
                db.commit()
                res = {
                    "stateCode": 200,
                    "message": "成功",
                    "data": "确认发货成功"
                }
            else:
                res = {
                    "stateCode": 202,
                    "message": "发货失败",
                    "data": "已发货，无需再次发货"
                }
        else:
            res = {
                "stateCode": 202,
                "message": "发货失败",
                "data": "订单未成功支付，无需发货"
            }
    else:
        res = {
            "stateCode": 202,
            "message": "发货失败",
            "data": "没有权限"
        }
    db.close()
    cursor.close()
    return res