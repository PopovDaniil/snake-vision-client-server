from queue import Queue
from signals import *
import zmq


def device_messaging_thread(data):
    context = zmq.Context()
    message_socket = context.socket(zmq.PUB)
    message_socket.connect('tcp://localhost:8888')
    message_socket.send_string(data)
    message_socket.close()
