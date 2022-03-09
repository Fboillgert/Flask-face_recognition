import os
import cv2
import math
import shutil
import numpy as np
from tqdm import tqdm
from pickle import dump
from model import db, gen_uuid, FaceAll, sql_inset_encodings
from datetime import datetime
from sklearn.neighbors import KNeighborsClassifier
from face_recognition.face_recognition_cli import image_files_in_folder
from face_recognition import load_image_file, face_locations, face_encodings
from app import train_path, abnormal_path


def file_getctime(file_path: str, face_name: str = None):
    dir_path, file_name = os.path.split(file_path)
    base_name, extension = os.path.splitext(file_name)
    try:
        create_time, file_face_name, rec, clarity = base_name.split('_')
        create_time = datetime.strptime(create_time, "%Y-%m-%d-%H-%M-%S-%f")
        face_id = gen_uuid()
    except ValueError:
        try:
            face_id, file_face_name, create_time = base_name.split('_')
            create_time = datetime.strptime(create_time, "%Y%m%d")
        except ValueError:
            try:
                face_id, create_time = base_name.split('_')
                create_time = datetime.strptime(create_time, "%Y%m%d")
                file_face_name = ''
            except ValueError:
                try:
                    face_id, file_face_name = base_name.split('_')
                    create_time = datetime.fromtimestamp(os.path.getctime(file_path))
                except ValueError:
                    year, mon, day, create_time, file_face_name, rec, clarity = base_name.split('-')
                    create_time = datetime.strptime(f'{year}-{mon}-{day}-{create_time}', "%Y-%m-%d-%H_%M_%S")
                    face_id = gen_uuid()
    if face_name is None:
        face_name = file_face_name
    file_name = f"{face_id}_{create_time.strftime('%Y%m%d')}.jpg"
    if not file_path.endswith(file_name):
        os.rename(file_path, os.path.join(dir_path, file_name))
        file_path = os.path.join(dir_path, file_name)
    return face_id, create_time, file_path, face_name


def get_known_face(power=False) -> dict:
    fa_file = dict()
    known_face = dict()
    fa_sql = {fa.face_id: fa for fa in FaceAll.query.filter_by(status=1).all()}
    # Loop through each person in the training set
    for class_dir in tqdm(os.listdir(train_path), desc='预处理', ncols=100, colour='CYAN'):
        if not os.path.isdir(os.path.join(train_path, class_dir)):
            continue
        # Loop through each training image for the current person
        for img_path in tqdm(image_files_in_folder(os.path.join(train_path, class_dir)), desc=class_dir, leave=False):
            face_id, create_time, img_path, face_name = file_getctime(img_path, face_name=class_dir)
            fa_file[face_id] = {'path': img_path, 'name': face_name, 'time': create_time}
            continue
    # --- 整理不存在的Model ---
    for i in fa_sql.keys() - fa_file.keys():
        fa_sql[i].status = 3
    db.session.commit()
    # --- 输出 user_name encodings ---
    for face_id in tqdm(fa_file.keys(), desc='整理中', ncols=100, colour='CYAN'):
        image = None
        encodings = None
        fa = fa_sql.get(face_id)
        if fa is None:
            fa = FaceAll.query.filter_by(face_id=face_id).first()
            if fa is None:
                image = load_image_file(fa_file[face_id]['path'])
                clarity = int(cv2.Laplacian(image, cv2.CV_64F).var())
                fa = FaceAll(
                    face_id=face_id, create_time=fa_file[face_id]['time'], user_name=fa_file[face_id]['name'], status=1,
                    rec=100, clarity=clarity
                )
                db.session.add(fa)
                db.session.commit()
        if fa.user_name != fa_file[face_id]['name']:
            fa.user_name = fa_file[face_id]['name']
        if power is False:
            encodings = fa.encodings()
        if encodings is None:
            if image is None:
                image = load_image_file(fa_file[face_id]['path'])
            face_bounding_boxes = face_locations(image, model="cnn")
            if len(face_bounding_boxes) == 1:
                encodings = face_encodings(image, known_face_locations=face_bounding_boxes)[0]
                sql_inset_encodings(face_id=face_id, encodings=encodings.tolist())
            else:
                fa.status = 2
                db.session.commit()
                shutil.move(
                    fa_file[face_id]['path'], os.path.join(abnormal_path, os.path.split(fa_file[face_id]['path'])[-1])
                )
                continue
        else:
            encodings = np.array(encodings)
        known_face[face_id] = (fa_file[face_id]['name'], encodings)
    return known_face


def train(known_face_names, known_face_encodings, save_path=None, n_neighbors=None, verbose=False):
    # Determine how many neighbors to use for weighting in the KNN classifier
    if n_neighbors is None:
        n_neighbors = int(round(math.sqrt(len(known_face_encodings))))
        if verbose:
            print("Chose n_neighbors automatically:", n_neighbors)

    # Create and train the KNN classifier
    knn_clf = KNeighborsClassifier(n_neighbors=n_neighbors, algorithm='ball_tree', weights='distance')
    knn_clf.fit(known_face_encodings, known_face_names)

    # Save the trained KNN classifier
    if save_path is not None:
        with open(save_path, 'wb') as f:
            dump(knn_clf, f)

    return knn_clf


if __name__ == '__main__':
    from app import model_save_path

    print("Training KNN classifier...")
    x = get_known_face(power=False)
    x_face_names = list()
    x_face_encodings = list()
    for key, item in x.items():
        x_face_names.append(key)
        x_face_encodings.append(item[1])
    classifier = train(x_face_names, x_face_encodings, save_path=model_save_path, n_neighbors=2)
    print("Training complete!")
