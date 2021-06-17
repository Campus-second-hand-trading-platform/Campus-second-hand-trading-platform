import datetime
import json
import time
from datetime import timedelta, date
import pymysql
from flask_cors import CORS
from flask import Flask, render_template, request, jsonify, Blueprint
from random import Random
from config import conn_db

manager = Blueprint('manager', __name__)
CORS(manager, supports_credentials=True)

@manager.route('/manager/login', methods=['POST'])
def Login():
    db = conn_db()  # 连接数据库
    cursor = db.cursor()  # 使用 cursor() 方法创建一个游标对象 cursor
    data = request.get_json(silent=True)
    managerid = data['mid']
    mpwd = data['mpwd']
    print(managerid)
    print(mpwd)
    search = "select * from manager where managerid='{}' and mpwd='{}'".format(managerid, mpwd)
    cursor.execute(search)
    db.commit()
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

##用户举报指定商品###
##################
@manager.route('/report', methods = ['POST'])
def PostReport():
    db = conn_db()  # 连接数据库
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
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



    create1 = "INSERT INTO report (reportid,uid,gid,rtime,rreason,rstate) values ("+ str(reportid) + ",'" + str(uid) + "'," + str(gid) + ",'" + timenowstr + "','" + rreason + "','" + "0" + "');"
    print(create1)
    cursor.execute(create1)
    db.commit()

    msg = {
        'data': "举报成功",
        'message': "成功",
        'stateCode': 200
    }
    return msg

# 管理员获得所有举报信息--done
@manager.route('/reports', methods=['GET'])
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
@manager.route('/reports/unsolved', methods = ['GET'])
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

# 管理员评判举报信息
@manager.route("report/<reportid>/result", methods=['PUT'])
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