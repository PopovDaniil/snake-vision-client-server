from queue import Queue
from threading import Thread

from device_messaging import device_messaging_thread
from image_detection import image_detection_thread
from ui import ui_thread

EXIT = 'EXIT'

def main():
    try:
        q = Queue()
        print('Client started')
        image_thr = Thread(target=image_detection_thread, name='Image detection', daemon=True)
        ui_thr = Thread(target=ui_thread, name='UI', args=(q,), daemon=True)
        image_thr.start()
        ui_thr.start()
        while True:
            if q.get() == EXIT:
                exit()
    except KeyboardInterrupt:
        exit()

if __name__ == '__main__':
    main()
