import base64
import ctypes
import time
from queue import Queue
from threading import Thread

import cv2
import numpy as np
import zmq
from ordered_set import OrderedSet

import HandTracking as htm
from gestures import gestures as all_gestures

EXIT = 'EXIT'

def image_detection_thread(queue: Queue):
    context = zmq.Context()
    image_socket = context.socket(zmq.SUB)
    image_socket.bind('tcp://*:7777')
    image_socket.setsockopt(zmq.SUBSCRIBE, b'')

    start_time = time.perf_counter()

    detector = htm.handDetector(detectionCon=0.85)

    tipIds = [4, 8, 12, 16, 20]

    found_gestures = dict()
    filtered_gestures = OrderedSet()

    print('Image detection started')

    def find_fingers(lmList: list):
        fingers = []
        if len(lmList) != 0:

                # Thumb
                if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)

                # 4 Fingers
                for id in range(1, 5):
                    if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                        fingers.append(1)
                    else:
                        fingers.append(0)
        return fingers

    def find_gesture(fingers: list, all_gestures: dict):
        for name in all_gestures:
            if all_gestures[name](fingers):
                return name

    def filter_gesture(gesture_name: str, found_gestures: dict[str,int], filtered_gestures: list[str]):
        found_gestures.setdefault(gesture_name, 0)
        found_gestures[gesture_name] += 1
        if found_gestures[gesture_name] >= 50:
            filtered_gestures.add(gesture_name)
            print(filtered_gestures)

    def find_sequence(gestures: list):
        if gestures == {'like', 'fist', 'hello'}:
            ctypes.windll.user32.MessageBoxW(0, "Лампочка гори!", "Действие", 1)
        return
        
    while True:
        start_tick = time.perf_counter()
        image_string = image_socket.recv_string()
        raw_image = base64.b64decode(image_string)
        image = np.frombuffer(raw_image, dtype=np.uint8)
        frame = np.array(cv2.imdecode(image, 1))
        img = detector.findHands(frame)
        lmList = detector.findPosition(img, draw=False)

        fingers = find_fingers(lmList)
        gesture_name = find_gesture(fingers, all_gestures)

        if gesture_name:
            filter_gesture(gesture_name, found_gestures, filtered_gestures)
            find_sequence(filtered_gestures)

        if cv2.waitKey(1) == 27:
            queue.put(EXIT)

        current_time = time.perf_counter()
        all_time = np.round(current_time - start_time, decimals=2)
        tick_time = current_time - start_tick
        tps = np.round(1 / tick_time, decimals=2)

        cv2.putText(img, f'Client time: {str(all_time)} ({tps} tps) ', (0, 100), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255))
        cv2.imshow("Image", img)
        cv2.waitKey(1)
        # pTime = cTime

def device_messaging_thread(queue: Queue):
    context = zmq.Context()
    message_socket = context.socket(zmq.PUB)
    message_socket.connect('tcp://localhost:8888')
    print('Device messaging started')

    while True:
        if (queue.get() == EXIT):
            message_socket.send_string(EXIT)
            print('EXIT sent')

def main():
    try:
        q = Queue()
        print('Client started')
        image_thr = Thread(target=image_detection_thread, name='Image detection', args=(q,), daemon=True)
        message_thr = Thread(target=device_messaging_thread, name='Device messaging', args=(q,), daemon=True)
        image_thr.start()
        message_thr.start()
        while True:
            if q.get() == EXIT:
                exit()
    except KeyboardInterrupt:
        exit()

if __name__ == '__main__':
    main()
