import datetime
import urllib.request
import json
import time
from datetime import timedelta
from urllib.parse import urljoin

import pymysql
from flask_cors import CORS
from flask import Flask, render_template, request, jsonify
from random import Random

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.debug = True
baseDir= "D://桌面//petshelperfront//"

# 连接数据库
db = pymysql.connect("localhost", "root", "123456", "petsHome")
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()


# 随机生成token
def get_token():
    length_r = 32
    token = ''
    chars = '01'
    length = len(chars) - 1
    random = Random()
    for i in range(length_r):
        token += chars[random.randint(0, length)]
    return token


# test  -----todo
@app.route('/test', methods=['GET'])
def test():
    data=request.args.get('type')
    print(data)
    res = {
        'status': 200,
        'msg': '登出成功'
    }

    return res

# 登录
@app.route('/login', methods=['POST', 'GET'])
def login():
    data = request.get_json(silent=True)
    username = data['username']
    password = data['password']
    print(username)
    # 使用 execute()  方法执行 SQL 查询
    sql = "select * from user where user = '" + username + "'"
    print(sql)
    cursor.execute(sql)

    # 使用 fetchone() 方法获取单条数据.
    data = cursor.fetchall()
    print(data)
    if len(data) == 0:
        res = {
            'status': 202,
            'msg': '不存在该用户'
        }
    else:
        if password != data[0][1]:
            res = {
                'status': 202,
                'msg': '密码错误'
            }
        else:
            # 获得新的token
            token = get_token()
            # 使用 execute()  方法执行 SQL 查询
            sql = "select * from token where username = '" + username + "'"
            print(sql)
            cursor.execute(sql)

            # 使用 fetchone() 方法获取单条数据.
            data = cursor.fetchall()
            print(data)
            if len(data) == 0:
                # 使用 execute()  方法执行 SQL 查询
                sql = "insert into token(username,token) values('" + username + "','" + token + "')"
                print(sql)
                cursor.execute(sql)
                db.commit()
                res = {
                    'status': 200,
                    'token': token,
                    'msg': '登陆成功'
                }
            else:
                # 该账号未登陆
                if len(data[0][1]) == 0:
                    # 使用 execute()  方法执行 SQL 查询
                    sql = "update token set token='" + token + "' where username= '" + username + "'"
                    print(sql)
                    cursor.execute(sql)
                    db.commit()
                    res = {
                        'status': 200,
                        'token': token,
                        'msg': '登陆成功'
                    }
                # 该账号未注销
                else:
                    res = {
                        'status': 202,
                        'token': token,
                        'msg': '登陆失败，账号已登录'
                    }

    return res


# 登出
@app.route('/logout', methods=['POST'])
def logout():
    data = request.get_json(silent=True)
    token = str(data['token'])
    sql = "update token set token='' where token= '" + token + "'"
    print(sql)
    cursor.execute(sql)
    db.commit()
    res = {
        'status': 200,
        'msg': '登出成功'
    }

    return res




# 游客留言  -----todo
@app.route('/visitorMessage', methods=['POST'])
def visitorMessage():
    data = request.get_json(silent=True)
    # {'email': '123', 'name': '张三', 'message': '11'}
    # print(data)
    nowtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql = "insert into notes values(%s,%s,%s,%s)"
    cursor.execute(sql, [data['email'], nowtime, data['name'], data['message']])
    db.commit()
    res = {
        'status': 200,
        'msg': '留言成功'
    }

    return res


# 发送博客所有
@app.route('/posts', methods=['GET'])
def posts():
    # 使用 execute()  方法执行 SQL 查询
    sql = "select * from blogs "
    print(sql)
    cursor.execute(sql)
    # 使用 fetchone() 方法获取单条数据.
    data = cursor.fetchall()
    print(data)
    temp = []
    for i in data:
        temp.append({
            'id': i[0],
            'title': i[1],
            'content': i[2],
            'username': i[3],
            'likes': i[4]
        })
    print(temp)
    res = {
        'status': 200,
        'blogs': temp
    }
    return res


# 发送指定博客
@app.route('/posts/<id>', methods=['GET'])
def postDetail(id):
    # 使用 execute()  方法执行 SQL 查询
    print(id);
    sql = "select * from blogs where id= " + str(id);
    print(sql)
    cursor.execute(sql)
    # 使用 fetchone() 方法获取单条数据.
    data = cursor.fetchall()
    print(data)
    print(data[0])
    temp = {
        'id': data[0][0],
        'title': data[0][1],
        'content': data[0][2],
        'username': data[0][3],
        'likes': data[0][4]
    }
    print(temp)
    res = {
        'status': 200,
        'post': temp
    }
    return res


# 发送指定博客
@app.route('/address', methods=['POST'])
def address():
    data = request.get_json(silent=True)
    print(data)
    # 获得user
    sql = "select username from token where token= '" + data['token'] + "'";
    # print(sql)
    cursor.execute(sql)
    temp = cursor.fetchall()
    print(temp)
    user = temp[0][0]
    # 把博客记录写入数据库
    sql = "insert into blogs(username,title,content) values('" + user + "','" + data['title'] + "','" + data[
        'content'] + "')"
    print(sql)
    cursor.execute(sql)
    db.commit()

    res = {
        'status': 200,
    }
    return res


# 发送宠物所有
@app.route('/pets', methods=['GET'])
def pets():
    # 使用 execute()  方法执行 SQL 查询
    sql = "select id,breed,age,sid,content,pic from pet "
    print(sql)
    cursor.execute(sql)
    # 使用 fetchone() 方法获取单条数据.
    data = cursor.fetchall()
    print(data)
    temp = []
    for i in data:
        temp.append({
            'id': i[0],
            'breed': i[1],
            'age': i[2],
            'from': i[3],
            'content': i[4],
            'pic': i[5]
        })
    print(temp)
    res = {
        'status': 200,
        'pets': temp
    }
    return res


# 发送指定宠物
@app.route('/pets/<id>', methods=['GET'])
def petDetail(id):
    # # 使用 execute()  方法执行 SQL 查询
    print(id);
    sql = "select * from pet where id=%s"
    cursor.execute(sql, id)
    info = cursor.fetchall()
    title = info[0][6]
    sex = info[0][3]
    time = info[0][8].strftime("%Y-%m-%d %H:%M:%S")
    breed = info[0][2]
    content = info[0][7]
    sid = info[0][1]
    pic = info[0][5]
    pname = info[0][11]
    if content is None:
        content = "无"

    sql1 = "select * from station where sid=%s"
    cursor.execute(sql1, sid)
    sinfo = cursor.fetchall()
    address = sinfo[0][2]
    homename = sinfo[0][1]
    linkname = sinfo[0][3]
    phone = sinfo[0][4]
    wechat = sinfo[0][5]
    if wechat is None:
        wechat = "无"
    temp = {
        'id': id,
        'title': title,
        'sex': sex,
        'time': time,
        'breed': breed,
        'from': address,
        'linkman': linkname,
        'phone': phone,
        'wechat': wechat,
        'content': content,
        'pic': pic,
        'homename': homename,
        'pname':pname if pname is not None else '暂无'
    }
    # print(temp)

    res = {
        'status': 200,
        'pet': temp
    }
    return res


# 领养表单处理
@app.route('/pets/adopt', methods=['POST'])
def adoptForm():
    data = request.get_json(silent=True)
    print(data)
    QQ = data['QQ']
    wechat = data['wechat']
    if QQ == '':
        QQ = None
    if wechat == '':
        wechat = None
    sql = "insert into request values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    cursor.execute(sql, [data['username'], data['petID'], datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                         data['name'], data['phone'], data['address'],
                         QQ, wechat, data['message']])
    db.commit()

    res = {
        'status': 200,
        'msg': '成功'
    }

    return res


# 我的领养请求 -----todo
@app.route('/adoptReq', methods=['POST'])
def adoptReq():
    data = request.get_json(silent=True)
    print(data)
    # {'username': 'admin'}
    user = data['username']
    sql = "select request.time,pet.content,pet.state,pet.user from request,pet where request.user=%s and " \
          "pet.id=request.id"
    print(sql)
    cursor.execute(sql, user)
    info = cursor.fetchall()
    print(info)
    temp = []
    for i in info:
        print(13)
        if i[3] == user:
            temp.append({
                "time": i[0].strftime("%Y-%m-%d %H:%M:%S"),
                "briefInfo": i[1],
                "state1": i[2],
                "state2": 1
            })
        else:
            print(13)
            temp.append({
                "time": i[0].strftime("%Y-%m-%d %H:%M:%S"),
                "briefInfo": i[1],
                "state1": i[2],
                "state2": 0
            })
    res = {
        'status': 200,
        'informs': temp
    }
    print(res)

    return res


# 点赞/取消点赞
@app.route('/like', methods=['POST'])
def like():
    data = request.get_json(silent=True)
    print(data)
    # 获得pet
    if data['op'] == '0':
        # 使用 execute()  方法执行 SQL 更新
        sql = "update blogs set likes=likes-1  where id= '" + str(data['id']) + "'"
        print(sql)
        cursor.execute(sql)
        db.commit()
        flag = 0
    elif data['op'] == '1':
        # 使用 execute()  方法执行 SQL 更新
        sql = "update blogs set likes=likes+1  where id= '" + str(data['id']) + "'"
        print(sql)
        cursor.execute(sql)
        db.commit()
        flag = 1
    else:
        flag = 2

        # 使用 execute()  方法执行 SQL 查询
    sql = "select * from blogs "
    print(sql)
    cursor.execute(sql)
    # 使用 fetchone() 方法获取单条数据.
    data = cursor.fetchall()
    print(data)
    temp = []
    for i in data:
        temp.append({
            'id': i[0],
            'title': i[1],
            'content': i[2],
            'username': i[3],
            'likes': i[4]
        })
    res = {
        'status': 200,
        'flag': flag,
        'blogs': temp
    }
    return res


# 注册
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json(silent=True)
    print(data)
    # 获得user
    sql = "select * from user where user= '" + data['username'] + "'"
    print(sql)
    cursor.execute(sql)
    temp = cursor.fetchall()
    print(temp)
    if len(temp) == 0:
        sql = "insert into user(user,password) values('" + data['username'] + "','" + data['password1'] + "')"
        print(sql)
        cursor.execute(sql)
        db.commit()
        res = {
            'status': 200,
            'msg': '注册成功'
        }
    else:
        res = {
            'status': 202,
            'msg': '该用户已存在'
        }
    return res


# # 救助站指定宠物领养请求查看 --todo
# @app.route('/home/pets/<id>/adoptCheck', methods=['GET'])
# def adoptReqCheck(id):
#     print(id)
#     # 前端发送来的数据---id（对应pet表中狗的id）
#
#     # 期待返回的数据
#     temp=[]
#     # temp:[
#     # {
#     #     'user':'admin',  谁发出的请求
#     #     'name':'李四',     联系人
#     #     'phone':'17854651665',
#     #     'address':'海淀区XXXX',
#     #     'content':'家在北京，同城，有稳定收入，巴拉巴拉',
#     # },
#     # ]
#     res = {
#         'status': 200,
#         'request': temp
#     }
#
#     return res
# # 救助站指定宠物领养请求确认 --todo
# @app.route('/home/pets/adoptConfirm', methods=['POST'])
# def adoptConfirm():
#     data = request.get_json(silent=True)
#     print(data)
#     # 前端发送来的数据
#     # data:{
#     #     'id':'1',   狗对应的id
#     #     'user':'admin',   确认领养的人的账户名
#     # }
#     # 期待返回的数据
#     res = {
#         'status': 200,
#         'msg': '成功'
#     }
#
#     return res
# 救助站登录 --todo
@app.route('/home/login', methods=['POST'])
def homeLogin():
    data = request.get_json(silent=True)
    status = 200
    sid = 0
    msg = '成功'
    phone = data['phone']
    pwd = data['password']
    print(phone, pwd)
    sql = "select sid,spassword from station where sphone=%s"
    ret = cursor.execute(sql, phone)  # 搜索是否存在该联系电话
    if ret > 0:  # 如果大于零，证明该救助站存在
        contents = cursor.fetchall()
        correctpwd = contents[0][1]
        if pwd == correctpwd:  # 账号密码全部正确
            sid = contents[0][0]
        else:
            status = 202
            msg = '密码错误'
    else:
        status = 202
        msg = '尚未注册'

    res = {
        'status': status,
        'sid': sid,
        'msg': msg
    }
    return res


# 救助站注册 --todo
@app.route('/home/register', methods=['POST'])
def homeRegister():
    data = request.get_json(silent=True)
    # 前端发送来的数据
    # data={
    #     'name':'加油宠物爱心小站',
    #     'address':'北京市朝阳区',
    #     'owner':'王晓红',
    #     'phone':'16626633366',# 直接以phone作为登录账户
    #     'wechat':'aixin123456',
    #     'password':'666666'
    # }
    sname = data['name']
    saddress = data['address']
    sowner = data['owner']
    sphone = data['phone']
    swechat = data['wechat']
    if swechat == '':
        swechat = None
    spassword = data['password1']

    status = 200
    msg = '成功'
    sql = "select * from station where sphone=%s"
    ret = cursor.execute(sql, sphone)  # 搜索是否存在该联系电话
    if ret > 0:  # 如果大于零，证明该救助站存在
        status = 202
        msg = '该救助站已注册'
    else:
        sql1 = "insert into station(sname,saddress,sowner,sphone,swechat,spassword) values (%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql1, [sname, saddress, sowner, sphone, swechat, spassword])
        db.commit()
    res = {
        'status': status,
        'msg': msg
    }
    return res


@app.route('/upload', methods=['GET', 'POST'])
def editorData():
    # 获取图片文件 name = upload
    img = request.files.get('file')
    # #额外参数--最大ID
    # maxID=request.form['maxID']
    # nextID=int(maxID)+1
    # print(nextID)
    # 图片名称
    imgName = img.filename
    url = baseDir + "//src//assets//images//pet" + str(int(getMaxID())+1)+".jpg"
    if img:
        f = open(url, 'wb')
    data = img.read()
    f.write(data)
    f.close()
    return 'url'
# 救助站宠物信息录入--获得自增长当前最大ID --todo
@app.route('/home/petsInforInput/getMaxID', methods=['GET'])
def getMaxID():
    sql="select max(id) from pet"
    cursor.execute(sql)
    data=cursor.fetchall()[0][0]
    return str(data)
# 救助站宠物信息录入 --todo
@app.route('/home/petsInforInput', methods=['POST'])
def petsInforInput():
    #获得数据
    data = request.get_json(silent=True)
    sid = data['sid']
    pname = data['name']
    breed = data['breed']
    sex = data['sex']
    age = data['age']
    if age == '':
        age = None
    pic = data['pic']
    content = data['content']
    pdetail = data['pdetail']
    if pdetail == '':
        pdetail = None
    ptime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    confirmtime = None
    state = 0
    user = None
    sql = "insert into pet(sid,pname,breed,sex,age,pic,content,pdetail,ptime,confirmtime,state,user) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    cursor.execute(sql, [sid, pname, breed, sex, age, pic, content, pdetail, ptime, confirmtime, state, user])
    db.commit()
    #保存图片
    sql = "select LAST_INSERT_ID() from pet" #获得最近插入的数据--线程安全
    cursor.execute(sql)
    id = cursor.fetchall()
    print(getMaxID())
    #保存本地地址至数据库--如果上传了图片的话
    try:
        file = open(baseDir + "//src//assets//images//pet" + str(getMaxID()) + ".jpg")
        sql = "update pet set pic=%s  where id=%s"
        cursor.execute(sql,
                       [str(getMaxID()), str(id[0][0])])
        db.commit()
        file.close()
    except FileNotFoundError:
        print("文件不存在")



    res = {
        'status': 200,
        'msg': '录入成功'
    }
    return res


# 救助站宠物信息查询 --todo
@app.route('/home/petsInforGet/<sid>', methods=['GET'])
def petsInforGet(sid):
    temp = []
    sql = "select id,pname,breed,sex,age,pic,ptime,confirmtime,user,content,pdetail,state from pet where sid=%s"
    ret = cursor.execute(sql, sid)
    if ret > 0:  # 如果该救助站录入过宠物信息
        content = cursor.fetchall()
        for row in content:
            id=row[0]
            pname=row[1]
            breed=row[2]
            sex=row[3]
            age = row[4]
            pic=row[5]
            pTime=row[6].strftime("%Y-%m-%d %H:%M:%S")
            state=row[11]
            content=row[9]
            pdetail=row[10]
            if age is None:
                age = '---'
            confirmtime = row[7]
            if confirmtime is None:
                confirmtime = '---'
            else:
                confirmtime = confirmtime.strftime("%Y-%m-%d %H:%M:%S")
            user = row[8]
            if user is None:
                user = '---'
            sql1 = "select COUNT(*) from request,pet,station where pet.id=request.id and station.sid=pet.sid and station.sid=%s and pet.id=%s group by station.sid,pet.id"
            print(sql1%(sid,row[0]))
            tempcur=cursor.execute(sql1, [sid, id])
            if tempcur>0:
                result = cursor.fetchall()
                print(result)
                reqNum = result[0][0]
            else:
                reqNum=0
            item = {
                'id': id,
                'pname': pname if pname else '---',
                'breed': breed,
                'age': age,
                'sex': sex,
                'pic': pic,
                'pTime': pTime,
                'confirmTime': confirmtime,
                'state':state,
                'user': user,
                'content': content  ,
                'pdetail': pdetail,
                'reqNum':reqNum
            }
            temp.append(item)
    # print(temp)
    res = {
        'status': 200,
        'pets': temp
    }

    return res

# 救助站宠物信息修改 --todo
@app.route('/home/petsInforGet/modify', methods=['POST'])
def petsInforModify():
    data = request.get_json(silent=True)
    print(data)
    # 前端发送来的数据
    # data:{
    #     'id':'1',   宠物对应的id
    #     'pname': '小黑2'  宠物名字
    #     'breed':'哈士奇',  宠物品种
    #     'age':'10',  宠物年龄
    #     'sex':'公',  宠物性别
    #     'pdetail':'巴拉巴拉'  宠物简述
    #     'content':'宠物的详细描述和领养要求'
    # }
    sql = "update pet set pname=%s, breed=%s, age=%s, sex=%s, pdetail=%s, content=%s  where id=%s"
    cursor.execute(sql, [str(data['pname']), str(data['breed']), str(data['age']), str(data['sex']), str(data['pdetail']),
                         str(data['content']), str(data['id'])])
    db.commit()
    res = {
        'status': 200,
        'msg': '修改成功'
    }
    return res




# 救助站宠物信息删除 --todo
@app.route('/home/petsInforGet/delete', methods=['POST'])
def petsInforDelete():
    data = request.get_json(silent=True)
    print(data)
    # 前端发送来的数据
    # data:{
    #     'id':'1',   宠物对应的id
    #     'pname': '小黑2'  宠物名字
    #     'breed':'哈士奇',  宠物品种
    #     'age':'10',  宠物年龄
    #     'sex':'公',  宠物性别
    #     'pdetail':'巴拉巴拉'  宠物简述
    #     'content':'宠物的详细描述和领养要求'
    # }

    sql = "delete from pet where id=%s"
    cursor.execute(sql, data['id'])
    db.commit()
    res = {
        'status': 200,
        'msg': '删除成功'
    }
    return res


# 救助站指定宠物领养请求查看 --todo
@app.route('/home/pets/<id>/adoptCheck', methods=['GET'])
def adoptReqCheck(id):
    # print(id)
    # 前端发送来的数据---id（对应pet表中狗的id）
    # 期待返回的数据
    # temp:[
    # {
    #     'user':'admin',  谁发出的请求
    #     'name':'李四',     联系人
    #     'phone':'17854651665',
    #     'address':'海淀区XXXX',
    #     'content':'家在北京，同城，有稳定收入，巴拉巴拉',
    # },
    # ]
    sql = "select state from pet where id=%s"
    ret = cursor.execute(sql, id)
    if ret > 0:
        state = cursor.fetchall()
    temp = []
    sql = "select user,rname,rphone,raddress,rcondition,time from request where id=%s"
    ret = cursor.execute(sql, id)
    if ret > 0:
        content = cursor.fetchall()
        for row in content:
            item = {
                'user': row[0],  # 谁发出的请求
                'name': row[1],  # 联系人
                'phone': row[2],
                'address': row[3],
                'content': row[4],
                'time': row[5].strftime("%Y-%m-%d %H:%M:%S")
            }
            temp.append(item)
    sql2 = "select state,user from pet where id=%s"
    cursor.execute(sql2, id)
    info=cursor.fetchall()
    temp2={
        'state':info[0][0],
        'user':info[0][1]
    }
    res = {
        'status': 200,
        'state' : state[0][0],
        'request': temp,
        'petInfo': temp2
    }
    return res


# 救助站指定宠物领养请求确认 --todo
@app.route('/home/pets/adoptConfirm', methods=['POST'])
def adoptConfirm():
    data = request.get_json(silent=True)
    # 前端发送来的数据
    # data={
    #     'id':'3',   #狗对应的id
    #     'user':'d'   #确认领养的人的账户名
    # }
    print(data)
    nowtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user = data['user']
    pid = data['id']
    sql = "update pet set state=1 where id=%s"
    cursor.execute(sql, pid)
    sql1 = "update pet set user=%s where id=%s"
    cursor.execute(sql1, [user, pid])
    sql2 = "update pet set confirmtime=%s where id=%s"
    cursor.execute(sql2, [nowtime, pid])
    db.commit()
    res = {
        'status': 200,
        'msg': '成功'
    }
    return res


# # 救助站自身资料修改 --todo
# @app.route('/home/informationModify', methods=['POST'])
# def informationModify():
#     data = request.get_json(silent=True)
#     print(data)
#     # 前端发送来的数据
#     # data:{
#     #     'sid':'1',   救助站对应的id
#     #     'sname':'海淀区救助站',
#     #     'saddress':'海淀区',
#     #     'sowner':'小明',
#     #     'sphone':'1784654981',注意手机号不能重复
#     #     'swechat':'1465',
#     #     'spassword':'123456',
#     # }
#     # 期待返回的数据
#     res = {
#         'status': 200,
#         'msg': '成功'
#     }
#
#     return res

# 救助站自身资料获得 --todo
@app.route('/home/informationGet/<id>', methods=['GET'])
def informationGet(id):
    sql = "select * from station where sid = %s"
    cursor.execute(sql, id)
    info = cursor.fetchall()
    temp = {
        'sname': info[0][1],
        'saddress': info[0][2],
        'sowner': info[0][3],
        'sphone': info[0][4],
        'swechat': info[0][5],
        'spassword': info[0][6],
    }
    res = {
        'status': 200,
        'form': temp
    }

    return res


# 救助站自身资料修改 --todo
@app.route('/home/informationModify', methods=['POST'])
def informationModify():
    data = request.get_json(silent=True)
    print(data)
    # 前端发送来的数据
    # data:{
    #     'sid':'1',   救助站对应的id
    #     'sname':'海淀区救助站',
    #     'saddress':'海淀区',
    #     'sowner':'小明',
    #     'sphone':'1784654981',注意手机号不能重复
    #     'swechat':'1465',
    #     'spassword':'123456',
    # }
    # 期待返回的数据
    sql = "select sname, saddress, sowner, sphone, swechat, spassword from station where sid = %s"
    cursor.execute(sql, data['sid'])
    info = cursor.fetchall()
    if info[0][3] == data['sphone']:
        if info[0][0] == data['sname'] and info[0][1] == data['saddress'] and info[0][2] == data['sowner'] and info[0][4] == data['swechat'] and info[0][5] == data['spassword']:
            res = {
                'status': 200,
                'msg': '手机号不能重复'
            }
        else:
            sql = "update station set sname=%s, saddress=%s, sowner=%s, swechat=%s, spassword=%s  where sid=%s"
            cursor.execute(sql, [data['sname'], data['saddress'], data['sowner'], data['swechat'], data['spassword'], data['sid']])
            db.commit()
            res = {
                'status': 200,
                'msg': '成功'
            }
    else:
        sql = "update station set sname=%s, saddress=%s, sowner=%s, sphone=%s, swechat=%s, spassword=%s  where sid=%s"
        cursor.execute(sql, [data['sname'], data['saddress'], data['sowner'], data['sphone'], data['swechat'], data['spassword'], data['sid']])
        db.commit()
        res = {
            'status': 200,
            'msg': '成功'
        }

    return res



if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True, port=5000)  # 启动socket
