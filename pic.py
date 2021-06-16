import datetime
import random
from werkzeug.utils import secure_filename
import os
from flask_cors import CORS
from flask import Flask, request, Blueprint,jsonify

pic = Blueprint('pic', __name__)
CORS(pic, supports_credentials=True)


UPLOAD_FOLDER = 'upload'
# pic.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
basedir = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'gif', 'GIF'])


def create_uuid():  # 生成唯一的图片的名称字符串，防止图片显示时的重名问题
    nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S");  # 生成当前时间
    randomNum = random.randint(0, 100);  # 生成的随机整数n，其中0<=n<=100
    if randomNum <= 10:
        randomNum = str(0) + str(randomNum);
    uniqueNum = str(nowTime) + str(randomNum);
    return uniqueNum;


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# 上传文件
@pic.route('/up_photo', methods=['POST'], strict_slashes=False)
def api_upload():
    # file_dir = os.path.join(basedir, pic.config['UPLOAD_FOLDER'])
    # file_dir = os.path.join(basedir, 'upload')
    file_dir=os.path.join('D:/桌面/campustradingplatform-front/src/assets/images/userImg/','upload')
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    f = request.files['file']
    if f and allowed_file(f.filename):
        # fname = secure_filename(f.filename)
        # print(fname)
        # ext = fname.rsplit('.', 1)[1]
        # new_filename = create_uuid() + '.' + ext
        # f.save(os.path.join(file_dir, new_filename))
        ext = f.filename.rsplit('.', 1)[1]
        new_filename = create_uuid() + '.' + ext
        f.save(os.path.join(file_dir, new_filename))
        #
        # filePath=file_dir+'/'+new_filename
        # print(filePath.replace("\\",'/'))
        # return jsonify({"success": 0, "msg": "上传成功"})
        return jsonify({"success": 0, "msg": "上传成功", "path":new_filename})
    else:
        return jsonify({"error": 1001, "msg": "上传失败"})


