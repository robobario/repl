from __future__ import print_function
from tornado.gen import Task, Return, coroutine
import tornado.process
import tornado.web
from tornado.ioloop import IOLoop
import re
from repl import Repl
import os.path
import time
import json 

repls = {}
pattern = re.compile(r"/(\d+)")
safe_repls = ["prolog","scala","python","haskell","ruby","clojure","erlang","kotlin","nodejs"]

def create_repl(ioloop,repl_type):
  global repls
  repl = Repl(ioloop, repl_type)
  repls[repl.identity] = repl
  return repl.identity

def clean_idle_repls():
  global repls
  try:
    to_del = []
    for key, repl in repls.iteritems():
      if repl.is_expired(): 
        to_del.append(key)
        repl.close()
    for key in to_del:
      del repls[key]
    ioloop = tornado.ioloop.IOLoop.current()
  finally:
    ioloop.call_later(2, clean_idle_repls)

class KillReplHandler(tornado.web.RequestHandler):
    def get(self, path):
        num = int(path)
        if num in repls:
            repls[num].close()
            del repls[num]
            self.set_status(200)
            self.finish() 
        else:
            self.clear()
            self.set_status(404)
            self.finish("<html><body>non existant repl type</body></html>")
class NewReplHandler(tornado.web.RequestHandler):
    def get(self, repl_type):
        if repl_type in safe_repls:
            repl_id = create_repl(ioloop, repl_type)
            self.write(json.dumps(repl_id))
        else:
            self.clear()
            self.set_status(404)
            self.finish("<html><body>non existant repl type</body></html>")

@tornado.web.stream_request_body
class MainHandler(tornado.web.RequestHandler):
    def get(self, path):
        num = int(path)
        if num not in repls:
            self.set_status(404)
        else:
            repls[num].drain_to_handler(self)

    def post(self, path):
        self.write("")

    def data_received(self, chunk):
        num = int(pattern.match(self.request.path).group(1))
        if num not in repls:
            self.set_status(404)
        else:
            repls[num].write_async(chunk)

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static")
}


class RootHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("static/index.html")


application = tornado.web.Application([
    (r"/", RootHandler),
    (r"/kill/(\d+)", KillReplHandler),
    (r"/(\d+)", MainHandler),
    (r"/new/([a-zA-Z0-9\-]+)", NewReplHandler),
], **settings)

if __name__ == "__main__":
    application.listen(8888)
    ioloop = tornado.ioloop.IOLoop.current()
    ioloop.call_later(5, clean_idle_repls)
    ioloop.start()
