import time
import tornado.process
import json

STREAM = tornado.process.Subprocess.STREAM
global_id = 0


def next_id():
    global global_id
    global_id += 1
    return global_id


def start(docker_tag):
    command = ["script", "-c" "docker run -t -i " + docker_tag, "/dev/null"]
    return tornado.process.Subprocess(command, stdin=STREAM,
                                      stdout=STREAM, stderr=STREAM)


class Repl:
    def __init__(self, ioloop, docker_tag):
        self.buffsize = 65536
        self.identity = next_id()
        self.ioloop = ioloop
        self.buff = bytearray(self.buffsize)
        self.offset = 0
        self.interpreter = start(docker_tag)
        self.ioloop.add_callback(self.start_fill)
        self.update_drain_time()

    def write_async(self, bytes):
        self.interpreter.stdin.write(bytes)

    def drain_to_handler(self, handler):
        to_write = bytes(self.buff[0:self.offset])
        handler.write(json.dumps(to_write))
        self.offset = 0
        if not self.interpreter.stdout.reading():
            self.ioloop.add_callback(self.start_fill)
        self.update_drain_time()

    def update_drain_time(self):
        self.last_drain_millis = time.time() * 1000.0

    def start_fill(self):
        self.buffer_filler(bytes())

    def write_to_buffer(self, immutable_bytes):
        self.buff[self.offset:self.offset + len(immutable_bytes)] = immutable_bytes
        self.offset += len(immutable_bytes)

    def buffer_filler(self, immutable_bytes):
        self.write_to_buffer(immutable_bytes)
        if (self.offset < self.buffsize):
            if not self.interpreter.stdout.reading():
                self.interpreter.stdout.read_bytes(self.buffsize - self.offset, partial=True,
                                                   callback=self.buffer_filler)
