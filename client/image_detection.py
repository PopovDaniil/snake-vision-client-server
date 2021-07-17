from queue import Queue

import zmq
import cv2
import time
import base64
import ctypes
import numpy as np
import HandTracking as htm
from gestures import gestures as all_gestures
from sequences import sequences as all_sequences, GestureSequence

def image_detection_thread(queue: Queue):
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

    def filter_gesture(gesture_name: str, found_gestures: dict[str,int], filtered_gestures: GestureSequence):
        found_gestures.setdefault(gesture_name, 0)
        found_gestures[gesture_name] += 1
        if found_gestures[gesture_name] >= 50:
            filtered_gestures.add(gesture_name)
            if gesture_name == 'clear':
                filtered_gestures.clear()
            print(filtered_gestures)

    def find_sequence(gestures: GestureSequence, all_sequences: dict):
        action = all_sequences.get(gestures)
        if action:
            ctypes.windll.user32.MessageBoxW(0, action(), "Действие", 1)
            return True
        return False

    context = zmq.Context()
    image_socket = context.socket(zmq.SUB)
    image_socket.bind('tcp://*:7777')
    image_socket.setsockopt(zmq.SUBSCRIBE, b'')

    start_time = time.perf_counter()

    detector = htm.handDetector(detectionCon=0.85)

    tipIds = [4, 8, 12, 16, 20]

    found_gestures = dict()
    filtered_gestures = GestureSequence()

    print('Image detection started')
        
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
            if find_sequence(filtered_gestures, all_sequences):
                filtered_gestures.clear()

        current_time = time.perf_counter()
        all_time = np.round(current_time - start_time, decimals=2)
        tick_time = current_time - start_tick
        tps = np.round(1 / tick_time, decimals=2)

        cv2.putText(img, f'Client time: {str(all_time)} ({tps} tps) ', (0, 100), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255))
        cv2.imshow("Image", img)
        cv2.waitKey(1)
        # pTime = cTime
