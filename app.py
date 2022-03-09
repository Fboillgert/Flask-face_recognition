#!/usr/bin/python3
import os
from pathlib import Path

from flask import Flask
from flask_compress import Compress
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

app = Flask(__name__)
Compress(app)


def mysql_path(password='your password', username="root", host="127.0.0.1", database="face_recognition"):
    engine = create_engine(f'mysql://{username}:{password}@{host}/{database}?charset=utf8mb4')
    if not database_exists(engine.url):
        create_database(engine.url, encoding='utf8mb4')
    return f'mysql://{username}:{password}@{host}/{database}?charset=utf8mb4'


face_folder = os.path.join(app.static_folder, 'image')
capture_face = os.path.join(face_folder, 'capture_face')
train_path = os.path.join(face_folder, 'knn_examples/train')
abnormal_path = os.path.join(face_folder, 'knn_examples/abnormal')
model_save_path = os.path.join(app.static_folder, 'trained_knn_model_cn.clf')
os.makedirs(face_folder, exist_ok=True)
os.makedirs(capture_face, exist_ok=True)
os.makedirs(train_path, exist_ok=True)
os.makedirs(abnormal_path, exist_ok=True)

app.config['SECRET_KEY'] = b'\x96\x17\xcd\x9a9\x0b(\xac^\x91\x1a\xf6\x18\x8c\xf7\xce'  # os.urandom(16)
app.config['JSON_AS_ASCII'] = False
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 86400
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 100
app.config['SCHEDULER_TIMEZONE'] = 'Asia/Shanghai'

app.config['SQLALCHEMY_DATABASE_URI'] = mysql_path()
# 动态追踪修改设置，如未设置只会提示警告
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# 查询时会显示原始SQL语句
app.config['SQLALCHEMY_ECHO'] = False
app.config['SQLALCHEMY_BINDS'] = {
    'face_all': mysql_path(),
    'face_encodings': mysql_path(),
}
db = SQLAlchemy(app, use_native_unicode='utf8mb4')


@app.url_defaults
def reverse_to_cache_busted_url(endpoint, values):
    if endpoint == 'static':
        if Path(values['filename']).suffix in ['.js', '.css', '.csv']:
            rooted_filename = os.path.join(app.static_folder, values['filename'])
            if os.path.exists(rooted_filename):
                values['q'] = int(os.stat(rooted_filename).st_mtime)
