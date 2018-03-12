import zmq
import sys
import time
import logging
import os

HOST = '127.0.0.1'
PORT = 4444

logging.basicConfig(filename='subscriber.log', level=logging.INFO)


class ZClient(object):

    def __init__(self, host=HOST, port=PORT):
        """Initialize Worker"""
        self.host = host
        self.port = port
        self._context = zmq.Context()
        self._subscriber = self._context.socket(zmq.SUB)
        self._pushing = self._context.socket(zmq.PUSH)

        print("Client Initiated")


    def send_message(self, pesan):
        try:
            url = 'tcp://{}:{}'.format(self.host, self.port+1)
            self._pushing.bind(url)
            time.sleep(1)
            print("sending message : {0}".format(pesan, self._pushing))
            self._pushing.send_multipart(pesan)

        except Exception as e:
            print("error {0}".format(e))

        finally:
            print("unbinding")
            self._pushing.unbind(url)


    def receive_message(self):
        """Start receiving messages"""
        self._subscriber.connect('tcp://{}:{}'.format(self.host, self.port))
        self._subscriber.setsockopt(zmq.SUBSCRIBE, b'baka')

        time.sleep(1)
        poller = zmq.Poller()
        poller.register(self._subscriber, zmq.POLLIN)
        poller.register(self._pushing, zmq.POLLIN)

        while True:
            print('listening on tcp://{}:{}'.format(self.host, self.port))
            events = poller.poll()
            time.sleep(1)
            if self._subscriber in dict(events):
                topic, message = self._subscriber.recv_multipart()
                self.send_message([topic, message])

            print('recving', events)
            print('recvd', message)
            logging.info(
                '{}   - {}'.format(message, time.strftime("%Y-%m-%d %H:%M")))

if __name__ == '__main__':
    zs = ZClient()
    zs.receive_message()
