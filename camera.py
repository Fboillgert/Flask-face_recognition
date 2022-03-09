import cv2
import requests
import threading
import numpy as np
from copy import deepcopy
from time import sleep, time
from json.decoder import JSONDecodeError
from datetime import datetime


class AutoFace:
    def __init__(self, video_url, time_range, show=False):
        self.show = show
        self.video_url = video_url
        self.image = None
        self.success = True
        self.movement = True
        self.th_read = threading.Thread(target=self.__read_image_thread, name='read')
        self.th_read.start()
        self.th_diff = threading.Thread(target=self.__diff_image_thread, name='diff')
        self.th_diff.start()

    def __read_image_thread(self, ret=True):
        self.logging(self.video_url, "启动摄像头~")
        cap = cv2.VideoCapture(self.video_url)
        while self.success and ret:
            ret, self.image = cap.read()
            # try:
            #     self.image = cv2.resize(image, (0, 0), fx=0.5, fy=0.5)
            # except Exception as ex:
            #     cap.release()
            #     self.logging("摄像头错误，正在重新启动摄像头~", ex)
            #     return self.__read_image_thread()
        cap.release()
        if self.success:
            self.logging("摄像头错误，正在重新启动摄像头~")
            return self.__read_image_thread()
        self.logging("已退出摄像头~")

    def __diff_image_thread(self, interval=0.1):
        self.logging("启动运动检测~")
        background = None
        while self.success:
            if self.image is None:
                continue
            frame = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            frame = cv2.GaussianBlur(frame, (21, 21), 0)
            if background is None:
                background = frame
                sleep(interval)
                continue
            diff = cv2.absdiff(background, frame)  # 检测背景和帧的区别
            diff = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]  # 二值化
            self.movement = True if np.count_nonzero(diff) else False
            background = None
        self.movement = True
        self.logging("已退出运动检测~")

    @staticmethod
    def logging(*args):
        print(datetime.now(), *args)

    def main(self):
        while self.success:
            while self.success and self.image is not None:
                frame = deepcopy(self.image)
                if self.movement:
                    t1 = time()
                    try:
                        for data in requests.post('http://127.0.0.1:8081/predict', files={
                            "file": cv2.imencode(".jpg", frame)[1].tobytes()
                        }, data={'save': 1, 'zoom': 50}, timeout=(2, 2)).json():
                            if self.show:
                                top, right, bottom, left = data['loc']
                                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 1)
                            print(data['face_name'], f'{data["rec"]}%', f'清晰度:{data["clarity"]}')
                    except (requests.exceptions.RequestException, JSONDecodeError):
                        pass
                    print(' ' * 20, time() - t1)
                if self.show:
                    cv2.imshow('small_frame', cv2.resize(frame, (0, 0), fx=0.5, fy=0.5))
                    k = cv2.waitKey(10) & 0xFF
                    if k == ord("q") or k == 27:
                        self.success = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.success = False
        self.th_diff.join()
        self.th_read.join()
        cv2.destroyAllWindows()
        self.logging("程序结束", exc_type, exc_val, exc_tb)


if __name__ == '__main__':
    with AutoFace(video_url=0, show=True) as af:
        af.main()
