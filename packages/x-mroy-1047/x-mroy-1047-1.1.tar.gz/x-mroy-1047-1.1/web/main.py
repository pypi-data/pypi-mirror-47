
#!/usr/bin/python
## write by qingluan
# just a run file
import tornado.ioloop
from tornado.ioloop import IOLoop
from web.setting import  appication, port
from qlib.io import GeneratorApi
import os


def main():
    args = GeneratorApi({
        'port':"set port ",
        })
    if args.port:
        port = int(args.port)
       	# os.popen('m-asyncs start')
    appication.listen(port)
    tornado.ioloop.IOLoop.instance().start()



if __name__ == "__main__":
    main()
