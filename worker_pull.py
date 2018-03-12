import zmq
import sys
import time
import logging
import os

HOST = '127.0.0.1'
PORT = 4445

logging.basicConfig(filename='subscriber.log', level=logging.INFO)


class ZClient(object):

    def __init__(self, host=HOST, port=PORT):
        """Initialize Worker"""
        self.host = host
        self.port = port
        self._context = zmq.Context()
        self._pulling = self._context.socket(zmq.PULL)

    def receive_pulling(self):
        url = 'tcp://{}:{}'.format(self.host, self.port)
        self._pulling.connect(url)

        time.sleep(1)
        poller = zmq.Poller()
        poller.register(self._pulling, zmq.POLLIN)

        while True:
            print('listening on {}'.format(url))
            events = poller.poll()
            time.sleep(1)
            if self._pulling in dict(events):
                topic, message = self._pulling.recv_multipart()

            print('recving', events)
            print('recvd', message)
            logging.info(
                '{}   - {}'.format(message, time.strftime("%Y-%m-%d %H:%M")))


if __name__ == '__main__':
    zs = ZClient()
    zs.receive_pulling()
