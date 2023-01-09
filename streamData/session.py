#!usr/bin/python
# -*- coding: utf-8 -*-
import httpx
from .config import Config

class Session(Config):

    def __init__(self, app = None):
        self.session = httpx.Client(http2 = True)
        Config.__init__(self, app)

    def request(self, method, url, *args, **kwargs):
        return self.session.request(method.upper(), url, *args, **kwargs)