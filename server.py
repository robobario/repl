from __future__ import print_function
from tornado.gen import Task, Return, coroutine
import tornado.process
import tornado.web
from tornado.ioloop import IOLoop
import re
from repl import Repl
repls = {}
pattern  = re.compile(r"/(\d+)")

@tornado.web.stream_request_body
class MainHandler(tornado.web.RequestHandler):
    def get(self, path):
        if self.get_argument("close", default=None) is not None:
          ioloop.stop()
        num = int(path)
        if num not in repls:
           repls[num] = Repl(ioloop, "python")
        repls[num].drain_to_handler(self)     
   
    def post(self, path):
        self.write("")

    def data_received(self, chunk):
        num = int(pattern.match(self.request.path).group(1))
        repls[num].write_async(chunk)

application = tornado.web.Application([
    (r"/(\d+)", MainHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    ioloop = tornado.ioloop.IOLoop.current()
    ioloop.start()