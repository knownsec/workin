#!/usr/bin/env python
# encoding: utf-8
import logging

import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options

from tornado.options import define, options

from workin.web import Application
from workin.database import Base

define("cmd", default='runserver',
            metavar="runserver",
            help=("Default use runserver"))
define("port", default=8000, help="default: 8000, required runserver", type=int)

if __name__ == '__main__':
    tornado.options.parse_command_line()

    app = Application('example.settings')
    if options.cmd == 'runserver':
        http_server = tornado.httpserver.HTTPServer(app)
        http_server.listen(options.port)
        logging.info('Web server listening on %s port.' % 8000)
        try:
            tornado.ioloop.IOLoop.instance().start()
        except KeyboardInterrupt:
            logging.warn('Exiting with keyboard interrupt.')
    elif options.cmd == 'syncdb':
        Base.metadata.create_all(bind=app.engine)
