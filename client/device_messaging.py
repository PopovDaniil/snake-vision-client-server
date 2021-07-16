from queue import Queue
from signals import *
import zmq


def device_messaging_thread(queue: Queue):
    context = zmq.Context()
    message_socket = context.socket(zmq.PUB)
    message_socket.connect('tcp://localhost:8888')
    print('Device messaging started')

    while True:
        if (queue.get() == EXIT):
            message_socket.send_string(EXIT)
            print('EXIT sent')
