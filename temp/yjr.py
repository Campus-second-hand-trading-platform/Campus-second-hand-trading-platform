import datetime
import json
import time
from datetime import timedelta, date
import pymysql
from flask_cors import CORS
from flask import Flask, render_template, request, jsonify, Blueprint
from random import Random

yjr = Blueprint('yjr', __name__)
CORS(yjr, supports_credentials=True)

def conn_db():
    # 连接数据库
    db = pymysql.Connect("localhost", "root", "123456", "ershou")
    return db


# 用户登陆
@yjr.route("/user/login", methods=['POST'])
def userLogin():
    db = conn_db()  # 连接数据库
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    data = request.get_json(silent=True)
    # data = {'userId': '18301001', 'password': '666666'}
    uno = data['userId']
    pwd = data['password']
    # print(uno, pwd)
    sql = "select uid,upwd from users where uid=%s"
    ret = cursor.execute(sql, [uno])  # 返回的影响的行数，如果是0，则是查询匹配结果为0行
    data = cursor.fetchall()
    if ret > 0:  # 有该用户
        if pwd != data[0][1]:
            res = {
                "stateCode": 202,
                "message": "密码错误"
            }
        else:
            res = {
                "stateCode": 200,
                "message": "登陆成功"
            }
    else:  # 没有该用户
        res = {
            "stateCode": 202,
            "message": "用户不存在"
        }
    # print(res)
    cursor.close()
    db.close()
    return res


# 注册
@yjr.route("/user/register", methods=['POST'])
def userRegister():
    db = conn_db()  # 连接数据库
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    data = request.get_json(silent=True)
    # data = {'userId': '18301011', 'password1': '111666',
    #         'password2': '111666', 'realname': '何丽',
    #         'nickname': '丽', 'phone': '98765434212',
    #         'department': '建筑与艺术学院'}
    uno = data['userId']
    pwd1 = data['password1']
    pwd2 = data['password2']
    name = data['realname']
    nickname = data['nickname']
    phone = data['phone']
    depart = data['department']
    # print(uno, pwd1, pwd2, name, nickname, phone, depart)
    if pwd1 != pwd2:
        res = {
            "stateCode": 202,
            "message": "失败",
            "data": "两次输入的密码不一致"
        }
    else:
        sql1 = "select * from users where uid=%s"
        ret = cursor.execute(sql1, [uno])
        if ret > 0:
            res = {
                "stateCode": 202,
                "message": "失败",
                "data": "该用户已注册"
            }
        else:
            sql = "insert into users(uid,upwd,uname,nickname,department,phone) values(%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, [uno, pwd1, name, nickname, depart, phone])
            db.commit()
            res = {
                "stateCode": 200,
                "message": "成功",
                "data": "注册成功"
            }
    # print(res)
    cursor.close()
    db.close()
    return res


# 修改用户信息
@yjr.route("/user/information", methods=['PUT'])
def modifyUserInfo():
    db = conn_db()  # 连接数据库
    cursor = db.cursor()  # 使用 cursor() 方法创建一个游标对象 cursor
    nickname = request.json.get("username")
    uid = request.json.get("userId")
    name = request.json.get("realname")
    phone = request.json.get("userPhone")
    signature = request.json.get("signature")  # 个性签名
    academy = request.json.get("department")
    sql = "update users set uname = %s,nickname=%s,department=%s,slogan=%s,phone=%s where uid=%s"
    cursor.execute(sql, [name, nickname, academy, signature, phone, uid])
    res = {
        "stateCode": 200,
        "message": "成功",
        "data": "身份信息修改成功"
    }
    db.commit()
    db.close()
    cursor.close()
    return res


# 买家取消订单支付-删除
@yjr.route("/order/cancel", methods=['PUT'])
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
@yjr.route("/order/drawback", methods=['GET'])
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


# 修改我的求购
@yjr.route("/seek/<id>", methods=['PUT'])
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


# 卖家修改商品接口
@yjr.route("/goods", methods=['PUT'])
def ModifyGoods():
    db = conn_db()  # 连接数据库
    cursor = db.cursor()  # 使用 cursor() 方法创建一个游标对象 cursor
    gid = request.json.get("gid")
    gname = request.json.get("gname")
    gprice = request.json.get("gprice")
    sellerid = request.json.get("sellerid")
    gtype = request.json.get("gtype")
    gdescription = request.json.get("gdescription")
    newness = request.json.get("newness")
    gcount = request.json.get("gcount")
    sql = "select * from goods where gid=%s and sellerid=%s"
    ret = cursor.execute(sql, [gid, sellerid])
    if ret > 0:
        sql1 = "select gstate,gcount from goods where gid=%s"
        cursor.execute(sql1, [gid])
        data = cursor.fetchall()
        gstate = data[0][0]  # 0已被买走（不管是否确认收货都是被买走）1未被买走
        # gcount = data[0][1]  # 0下架（自己下架/被举报而下架）1上架
        if gstate == 1:
            sql2 = "update goods set gname=%s,gprice=%s,gtype=%s,gdescription=%s,newness=%s,gcount=%s where gid=%s"
            cursor.execute(sql2, [gname, gprice, gtype, gdescription, newness,gcount, gid])
            db.commit()
            res = {
                "stateCode": 200,
                "message": "成功",
                "data": "商品信息修改成功"
            }
        else:
            res = {
                "stateCode": 202,
                "message": "失败",
                "data": "商品已经售出，不可修改"
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


# 卖家下架商品接口--todo
@yjr.route("/goods/<gid>", methods=['DELETE'])
def dropGoods(gid):
    db = conn_db()  # 连接数据库
    cursor = db.cursor()  # 使用 cursor() 方法创建一个游标对象 cursor
    sql = "select gstate from goods where gid=%s"
    cursor.execute(sql, [gid])
    data = cursor.fetchall()
    gstate = data[0][0]  # 看商品是否被买走
    if gstate == 1:  # 未被买走,直接下架
        cancel_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql2 = "update goods set gcount=%s,remove_time=%s where gid=%s"
        cursor.execute(sql2, [0, cancel_time, gid])
        db.commit()
        res = {
            "stateCode": 200,
            "message": "成功",
            "data": "商品未被购买，下架成功"
        }
    else:  # 如果被买走了
        sql3 = "select confirm from orders where gid=%s and ostate=%s"
        cursor.execute(sql3, [gid, 1])
        data1 = cursor.fetchall()
        confirm = data1[0][0]  # 看是否被确认收货
        if confirm == 1:  # 如果被确认收货了
            canceltime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sql4 = "update goods set gcount=%s,remove_time=%s where gid=%s"
            cursor.execute(sql4, [0, canceltime, gid])
            db.commit()
            res = {
                "stateCode": 200,
                "message": "成功",
                "data": "商品已确认收货，下架成功"
            }
        else:  # 商品被购买了但还未确认收货
            res = {
                "stateCode": 202,
                "message": "失败",
                "data": "商品还未被确认收货，下架失败"
            }
    db.close()
    cursor.close()
    return res


# 管理员评判举报信息
@yjr.route("report/<reportid>/result", methods=['PUT'])
def manageReport(reportid):
    db = conn_db()  # 连接数据库
    cursor = db.cursor()  # 使用 cursor() 方法创建一个游标对象 cursor
    result = request.json.get("result")  # reportid举报信息的评判结果
    sql = "select rstate from report where reportid=%s"
    cursor.execute(sql, [reportid])
    data = cursor.fetchall()
    cur = data[0][0]
    if cur == 0:  # 未审批过
        sql1 = "update report set rstate=%s where reportid=%s"
        cursor.execute(sql1, [result, reportid])
        db.commit()
        res = {
            "stateCode": 200,
            "message": "成功",
            "data": "评价成功"
        }
    else:
        res = {
            "stateCode": 202,
            "message": "失败",
            "data": "已审批过，评价失败"
        }
    db.close()
    cursor.close()
    return res

# 评论求购
@yjr.route("/seek/comment", methods=['POST'])
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


# 卖家确认订单发货接口
@yjr.route("/order/beginDelivery", methods=['PUT'])
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