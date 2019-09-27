'''
-*- coding: utf-8 -*-
@Author  : LiZhichao
@Time    : 2019/8/18 6:44
@Software: PyCharm
@File    : webApp.py
'''
import time
#处理特定请求的模块
def app(environ,start_response):
    status = "200 OK"
    response_headers = [('Content-Type','text/plain;charset=UTF-8')]
    start_response(status,response_headers)
    return "\n========简单的APP程序========\n%s"%time.ctime()