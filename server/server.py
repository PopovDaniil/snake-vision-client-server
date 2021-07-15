import base64
import signal
from queue import Queue
from threading import Thread
import time

import cv2
import numpy as np
import zmq

EXIT = 'EXIT'

def image_detection_thread(queue: Queue):
    context = zmq.Context()
    image_socket = context.socket(zmq.PUB)
    image_socket.connect('tcp://localhost:7777')

    start_time = time.perf_counter()
    camera = cv2.VideoCapture(0)
    print('Image sending started')
    while True:
        start_tick = time.perf_counter()
        try:
            ret, frame = camera.read()
            frame = cv2.resize(frame, (640, 480))

            current_time = time.perf_counter()
            all_time = np.round(current_time - start_time, decimals=2)
            tick_time = current_time - start_tick
            tps = np.round(1 / tick_time, decimals=2)

            cv2.putText(frame, f'Server time: {str(all_time)} ({tps} tps)', (0, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255))
            encoded, buf = cv2.imencode('.jpg', frame)
            image = base64.b64encode(buf)
            image_socket.send(image)
        except KeyboardInterrupt:
            camera.release()
            cv2.destroyAllWindows()

def device_messaging_thread(queue: Queue):
    context = zmq.Context()
    message_socket = context.socket(zmq.SUB)
    message_socket.bind('tcp://*:8888')
    message_socket.setsockopt(zmq.SUBSCRIBE, b'')
    print('Device messaging started')

    while True:
        reply = message_socket.recv_string()
        print(reply)
        if reply == EXIT:
            print('EXIT received')
            queue.put(EXIT)

def main():
    try:
        print('Server started')
        q = Queue()
        image_thr = Thread(target=image_detection_thread, name='Image sending', args=(q,), daemon=True)
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
