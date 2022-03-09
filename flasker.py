#!/usr/bin/python3
from app import app, model_save_path
from waitress import serve
from threading import Thread
from pickle import load as pickle_load
from extract_face import get_known_face, train

from unit_face import face


def async_code(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()

    return wrapper


@async_code
def custom_call():
    with open(model_save_path, 'rb') as f:
        app.config['classifier'] = pickle_load(f)
    app.config['known_face'] = get_known_face()
    x_face_names = list()
    x_face_encodings = list()
    for key, item in app.config['known_face'].items():
        x_face_names.append(key)
        x_face_encodings.append(item[1])
    app.config['classifier'] = train(x_face_names, x_face_encodings, save_path=model_save_path)


app.register_blueprint(face)

if __name__ == "__main__":
    custom_call()
    serve(app, threads=5, listen='*:8081')
