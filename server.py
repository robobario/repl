from __future__ import print_function
from tornado.gen import Task, Return, coroutine
import tornado.process
import tornado.web
from tornado.ioloop import IOLoop
import re
from repl import Repl
import os.path
import time

repls = {}
pattern = re.compile(r"/(\d+)")

def clean_idle_repls():
  global repls
  to_del = []
  for key, repl in repls.iteritems():
    if repl.is_expired(): 
       to_del.append(key)
       repl.close()
  for key in to_del:
    del repls[key]
  ioloop = tornado.ioloop.IOLoop.current()
  ioloop.call_later(2, clean_idle_repls)

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


settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static")
}


class RootHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("static/index.html")


application = tornado.web.Application([
    (r"/", RootHandler),
    (r"/(\d+)", MainHandler),
], **settings)

if __name__ == "__main__":
    application.listen(8888)
    ioloop = tornado.ioloop.IOLoop.current()
    ioloop.call_later(5, clean_idle_repls)
    ioloop.start()
