import asyncio
import uvloop

import zmq
from zmq.asyncio import Poller, Context

from sanic import Sanic
from sanic.response import text, stream
# loop = ioloop.IOLoop.instance()

HOST = '127.0.0.1'
PULL = 4445
PUB = 4444
url = 'tcp://{}:{}'.format(HOST, PULL)
url_pub = 'tcp://{}:{}'.format(HOST, PUB)

looper = uvloop.new_event_loop()
asyncio.set_event_loop(looper)

ctx = Context.instance()
publisher = ctx.socket(zmq.PUB)
publisher.bind(url_pub)

app = Sanic()


@app.route('/push')
async def send_message(req):
    pesan = req.args.get('message')

    """sending messages with pub"""
    msg = "sending message : {0}".format(pesan, publisher)
    print("sending message : {0}".format(pesan, publisher))
    await publisher.send_multipart([b'baka', pesan.encode('utf-8')])
    await asyncio.sleep(0.5)
        # publisher.unbind(url_pub)
    return text(msg)


@app.route('/stream', stream=True)
async def async_stream(req):
    async def receiver(response):
        print('listening on {}'.format(url))
        """receive messages with polling"""
        pull = ctx.socket(zmq.PULL)
        pull.connect(url)
        poller = Poller()
        poller.register(pull, zmq.POLLIN)
        while True:
            body = await req.stream.get()
            events = await poller.poll()
            msg = await pull.recv_multipart() if pull in dict(events) else 'waiting ...'
            response.write(msg)
    return stream(receiver)


@app.route('/')
async def home(req):
    return text('Selamat Datang')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090)

