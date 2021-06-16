import pymysql



def conn_db():
    # 连接数据库
    db = pymysql.Connect("localhost", "root", "123456", "ershou")
    return db