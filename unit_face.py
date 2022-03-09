import os
import cv2
import shutil
import numpy as np
from extract_face import train
from datetime import datetime, timedelta
from model import db, gen_uuid, FaceAll, sql_inset_data
from app import app, face_folder, capture_face, train_path
from face_recognition import load_image_file, face_locations, face_encodings
from flask import Blueprint, request, jsonify, send_from_directory, render_template, abort, redirect, url_for

face = Blueprint('face', __name__, url_prefix='/')


class TrainModel:

    def __init__(self, face_id: str):
        self.face_id = face_id
        self.file_path = find_image(self.face_id)
        self.dir_path, self.file_name = os.path.split(self.file_path)
        self.data = FaceAll.query.filter_by(face_id=face_id).first()

    def move(self, user_name: str = None):
        if user_name is None:
            user_name = self.data.user_name
        folder_path = os.path.join(train_path, user_name)
        os.makedirs(folder_path, exist_ok=True)
        new_path = os.path.join(folder_path, self.file_name)
        shutil.move(self.file_path, new_path)
        self.file_path = new_path
        self.dir_path, self.file_name = os.path.split(self.file_path)
        self.data.user_name = user_name
        self.data.status = 1
        db.session.commit()
        app.config['known_face'][self.face_id] = (user_name, np.array(self.data.encodings()))

    def delete(self):
        db.session.delete(self.data)
        db.session.commit()
        os.remove(self.file_path)


def find_image(file_uuid: str = None, file_name: str = None):
    if file_name is not None:
        for root, dirs, files in os.walk(face_folder):
            if os.path.exists(os.path.join(root, file_name)):
                return os.path.join(root, file_name)
    if file_uuid is not None:
        for root, dirs, files in os.walk(face_folder):
            for file in files:
                if file.startswith(file_uuid):
                    return os.path.join(root, file)
    return None


def get_face_name(face_id: str) -> str:
    try:
        face_name = app.config['known_face'][face_id][0]
    except KeyError:
        face_name = FaceAll.query.filter_by(face_id=face_id).first().user_name
    return face_name


def enlarge_loc(loc, iw, ih):
    top, right, bottom, left = loc
    l_x = int((bottom - top) / 2)
    l_y = int((right - left) / 2)
    left = max(left - l_y, 0)
    top = max(top - l_x, 0)
    right = min(right + l_y, iw)
    bottom = min(bottom + l_x, ih)
    return top, right, bottom, left


def predict_read(image):  # 载入图片数据
    if isinstance(image, str):
        try:
            image = load_image_file(find_image(image))
        except (FileNotFoundError, AttributeError):
            return []
    return image


def predict(image, save: bool = False, zoom: int = 100) -> list:
    loc_list = list()
    image = predict_read(image)
    zoom = float(zoom / 100)
    small_image = cv2.resize(image, (0, 0), fx=zoom, fy=zoom)
    faces_locations = face_locations(small_image, model='cnn')
    if len(faces_locations):
        ih, iw, ic = small_image.shape
        faces_encodings = face_encodings(small_image, known_face_locations=faces_locations)
        closest_distances = app.config['classifier'].kneighbors(faces_encodings, n_neighbors=1)
        for face_from, loc, rec, encodings in zip(
                app.config['classifier'].predict(faces_encodings), faces_locations, closest_distances[0],
                faces_encodings
        ):
            face_name = get_face_name(face_from)
            top, right, bottom, left = enlarge_loc(loc, iw, ih)
            top = int(top * (1 / zoom))
            right = int(right * (1 / zoom))
            bottom = int(bottom * (1 / zoom))
            left = int(left * (1 / zoom))
            face_frame = image[top:bottom, left:right]
            clarity = int(cv2.Laplacian(face_frame, cv2.CV_64F).var())  # 脸部模糊度
            now_time = datetime.now()
            rec = int((1 - rec) * 100)
            face_id = gen_uuid()
            file_name = f"{face_id}_{now_time.strftime('%Y%m%d')}.jpg"
            loc_list.append({
                'face_name': face_name,
                'from': face_from,
                'rec': rec,
                'clarity': clarity,
                'uuid': face_id,
                'time': now_time,
                'loc': (top, right, bottom, left),
            })
            if save and clarity >= 200:
                sql_inset_data(
                    face_id=face_id, create_time=now_time, user_name=face_name, rec=rec, clarity=clarity,
                    encodings=encodings.tolist(), status=0
                )
                cv2.imencode('.jpg', face_frame)[1].tofile(os.path.join(capture_face, file_name))
    return loc_list


@face.route('/', methods=['GET'])
@face.route('/index.html', methods=['GET'])
def index():
    return '<br/>'.join(
        [f'<a href="{value[0].rule}">{key}</a>' for key, value in app.url_map._rules_by_endpoint.items()]
    )


@face.route('/train', methods=['GET'])
def unit_train():
    x_face_names = list()
    x_face_encodings = list()
    for key, item in app.config['known_face'].items():
        x_face_names.append(key)
        x_face_encodings.append(item[1])
    app.config['classifier'] = train(x_face_names, x_face_encodings)
    return 'success'


@face.route('/show/image', methods=['GET'])
def show_image():
    file_name = request.values.get('file', '').strip()
    file_uuid = request.values.get('uuid', '').strip()
    file_path = None
    if file_name:
        file_path = find_image(file_name=file_name)
    elif file_uuid:
        file_path = find_image(file_uuid=file_uuid)
    else:
        abort(404)
    if file_path is not None:
        dir_path, filename = os.path.split(file_path)
        return send_from_directory(dir_path, filename)
    abort(404)


@face.route('/predict', methods=['GET', 'POST'])
def predict_image():
    if request.method == 'GET':
        image = request.values.get('image')
        if not image:
            abort(500)
    else:
        file = request.files.get('file')
        image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
    save = True if request.values.get('save', 0, type=int) else False
    zoom = max(min(100, request.values.get('zoom', 100, type=int)), 1)
    return jsonify(predict(image, save=save, zoom=zoom))


@face.route('/image/train', methods=['GET', 'POST'])
def image_train():
    if request.method == 'GET':
        time_range = request.values.get('time')
        num = request.values.get('num', 5, type=int)
        if time_range is None:
            target_time = datetime.now().strftime("%Y%m%d")
            return redirect(url_for('face.image_train', num=num, time=target_time))
        unit_train()
        try:
            min_time, max_time = time_range.split('-')
        except ValueError:
            min_time = max_time = time_range
        min_time = datetime.strptime(min_time, "%Y%m%d")
        max_time = datetime.strptime(max_time, "%Y%m%d")
        yesterday = (min_time - timedelta(days=1)).strftime("%Y%m%d")
        tomorrow = (max_time + timedelta(days=1)).strftime("%Y%m%d")
        data = FaceAll.query.filter(
            FaceAll.create_time >= min_time.replace(hour=0, minute=0, second=0),
            FaceAll.create_time <= max_time.replace(hour=23, minute=59, second=59),
            FaceAll.clarity >= 1000
        ).order_by(FaceAll.clarity.desc(), FaceAll.rec.desc()).all()
        results = dict()
        for item in data:
            if item.user_name in results:
                if not len(results[item.user_name]) >= num:
                    results[item.user_name].append(item)
            else:
                results[item.user_name] = [item]
        return render_template('image_train.html', results=results, yesterday=yesterday, tomorrow=tomorrow, num=num)
    else:
        face_id = request.values.get('id', '').strip()
        user_name = request.values.get('value', '').strip()
        if face_id:
            if user_name:
                TrainModel(face_id).move(user_name=user_name)
            else:
                TrainModel(face_id).delete()
        return 'success'


@face.route('/image/knn', methods=['GET', 'POST'])
def image_knn():
    face_id = request.values.get('id')
    if face_id is not None:
        fa = FaceAll.query.filter_by(face_id=face_id).first()
        if fa is not None:
            face_from = app.config['classifier'].predict(np.array(fa.encodings()).reshape(1, -1))[0]
            face_name = get_face_name(face_from)
            fa.user_name = face_name
            db.session.commit()
            return jsonify(face_name=face_name, face_from=face_from, img_url=url_for('face.show_image', uuid=face_from))
    abort(405)
