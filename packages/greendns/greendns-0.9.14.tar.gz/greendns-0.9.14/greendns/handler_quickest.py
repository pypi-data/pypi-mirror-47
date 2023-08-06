# -*- coding: utf-8 -*-
import logging
from greendns import handler_base
from greendns import session
from greendns import connection


class QuickestSession(session.Session):
    def __init__(self):
        super(QuickestSession, self).__init__()


class QuickestHandler(handler_base.HandlerBase):
    def __init__(self):
        self.logger = logging.getLogger()
        self.upstreams = ""
        self.servers = []

    def add_arg(self, parser):
        parser.add_argument("--upstreams",
                            help="Specify upstream dns servers",
                            default="223.6.6.6:53,114.114.114.114:53")

    def parse_arg(self, parser, remaining_argv):
        myargs = parser.parse_args(remaining_argv)
        self.upstreams = myargs.upstreams

    def init(self, io_engine):
        for upstream in self.upstreams.split(','):
            addr = connection.parse_addr(upstream)
            if addr is None:
                return []
            self.servers.append(addr)
        return self.servers

    def new_session(self):
        return QuickestSession()

    def on_upstream_response(self, sess, addr):
        for _, data in sess.server_resps.items():
            return data
        return ""
