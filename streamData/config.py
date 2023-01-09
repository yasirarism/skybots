#!usr/bin/python
# -*- coding: utf-8 -*-
import livejson

class Config(object):

    HONEY_HOST = "https://wjxwd01mwyo.dt01showxx02.com"
    MANGO_HOST = "https://api.yogurtlive.me"
    THAI69HOST = "https://ng01.baiyifuhaoc.com"

    HONEY_HEADERS = {
        "User-Agent": "HS-Android Mozilla/5.0 (Linux; Android 7.0; Redmi Note 4 Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/97.0.4692.98 Mobile Safari/537.36",
        "BundleIdentifier": "user",
        "Accept-Encoding": "identity",
        "X-Token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJuYmYiOjE2NDMzNTI1MDkuNjk1MTY1LCJpYXQiOjE2NDMzNTI1MDkuNjk1MTY1LCJleHAiOjE2NDQ1NjIxMDkuNjk1MTY1LCJpZCI6MjU1NzU4NSwic2hvd19pZCI6IjEyNTUwMDk2NzMiLCJzdGF0dXMiOjEsInR5cGUiOjIsImxldmVsIjoxLCJ2aXAiOjEsInBob25lX2lzX2JpbmRlZCI6MiwiZW1haWxfaXNfYmluZGVkIjoyLCJsYXN0X2FjdGl2ZV9kZXZpY2UiOjF9.WDELXGs8xvJW3v8lV_hu4HMlLW7E33fM1pohp7f2gw0",
        "X-Version": "2.10.1.4",
        "Connection": "Keep-Alive"
    }

    MANGO_HEADERS = {
        "Content-Type": "application/json",
        "accept": "application/json",
        "user-agent": "okhttp/3.2.1"
    }

    THAI69_HEADERS = {
        "token": "d33ca0ca9b904b43aa016ecf7f9c3a0e0BcMM",
        "nbnb": "verynb",
        "version": "2.1.20.1",
        "content-type": "application/json; charset=UTF-8"
    }

    def __init__(self, app = None):
        if not app:
            self.headers  = livejson.File("database.json", True, True, 4)
            self.host_url = None
        elif app.upper() == "MANGO":
            self.headers  = self.MANGO_HEADERS
            self.host_url = self.MANGO_HOST
        elif app.upper() == "HONEY":
            self.headers  = self.HONEY_HEADERS
            self.host_url = self.HONEY_HOST
        elif app.upper() == "THAI_69":
            self.headers  = self.THAI69_HEADERS
            self.host_url = self.THAI69HOST