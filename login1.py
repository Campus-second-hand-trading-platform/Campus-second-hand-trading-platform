import datetime
import json
import time
from datetime import timedelta, date
import pymysql
from flask_cors import CORS
from flask import Flask, render_template, request, jsonify, Blueprint
from random import Random
from config import conn_db

login1 = Blueprint('login1', __name__)
CORS(login1, supports_credentials=True)


# 用户登陆
@login1.route("/user/login", methods=['POST'])
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
@login1.route("/user/register", methods=['POST'])
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
@login1.route("/user/information", methods=['PUT'])
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


@login1.route('/user/information', methods=['GET'])
def Userinfo():
    db = conn_db()  # 连接数据库
    cursor = db.cursor()  # 使用 cursor() 方法创建一个游标对象 cursor
    uid = request.args.get("userId")
    search = "select * from users where uid='{}'".format(uid)
    cursor.execute(search)
    db.commit()
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
