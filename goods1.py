import datetime
import json
import time
from datetime import timedelta, date
import pymysql
from flask_cors import CORS
from flask import Flask, render_template, request, jsonify, Blueprint
from random import Random
from config import conn_db

goods1 = Blueprint('goods1', __name__)
CORS(goods1, supports_credentials=True)


# #获得某一类型的所有商品--done
@goods1.route('/goods', methods=['GET'])
def goods():
    db = conn_db()  # 连接数据库
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # 获取前端数据
    gtype = request.args.get("type")
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


##搜索获得商品##
@goods1.route('/goods/search', methods=['GET'])
def searchGoods():
    db = conn_db()  # 连接数据库
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    searchKey = request.args.get("searchKey")
    print(searchKey)
    create1 = "select * from goods where gname like '%" + searchKey + "%';"
    print(create1)
    cursor.execute(create1)
    db.commit()
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
            'upload_time': i[8],
            'remove_time': i[9],
            'picture': i[10],
            'morepic': i[11],
            'newness': i[12]

        })
    msg = {
        'data': tmp,
        'message': "成功",
        'stateCode': 200
    }
    return msg


# 卖家发布商品--done
@goods1.route('/goods', methods=['POST'])
def goodsSeller():
    db = conn_db()  # 连接数据库
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
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
    db.commit()

    msg = {
        'stateCode': 200,
        'message': "成功",
        'data': "上架商品成功"
    }
    return msg


# 卖家获得我的商品信息
@goods1.route('/seller/goods', methods=['GET'])
def sellergoods():
    db = conn_db()  # 连接数据库
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
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


# 卖家修改商品接口
@goods1.route("/goods", methods=['PUT'])
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
            cursor.execute(sql2, [gname, gprice, gtype, gdescription, newness, gcount, gid])
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
@goods1.route("/goods/<gid>", methods=['DELETE'])
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


# 获得指定商品信息
@goods1.route('/goods/<goodsId>', methods=['GET'])
def goodDetail(goodsId):
    db = conn_db()  # 连接数据库
    cursor = db.cursor()  # 使用 cursor() 方法创建一个游标对象 cursor
    print(goodsId)
    search = "select * from goods where gid='{}'".format(goodsId)
    cursor.execute(search)
    db.commit()
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
    db.commit()
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
