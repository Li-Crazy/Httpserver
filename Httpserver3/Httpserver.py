'''
#coding: utf-8
功能：完成httpserver部分
@Author  : LiZhichao
@Time    : 2019/8/29 14:28
@Software: PyCharm
@File    : Httpserver.py
'''
from socket import *
import sys
import os
import re
import time
from threading import Thread
# from Httpserver3.WebFramework import app

# 设置静态文件文件夹
# HTML_ROOT_DIR = './static'

# 处理HTTP请求
class HTTPserver(object):
    def __init__(self,app):
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.app = app

    def bind(self,addr):
        self.sockfd.bind(addr)

    def start(self):
        self.sockfd.listen(10)
        while True:
            c,addr = self.sockfd.accept()
            print(addr,"用户连接")
            handler_thread = Thread(target=self.handler_client,args=(c,))
            handler_thread.start()

    # 客户端处理函数
    def handler_client(self,c):
        # 接收浏览器request
        request_data = c.recv(2048)
        request_lines = request_data.splitlines()
        # 请求行 'GET /*** HTTP/1.1
        request_line = request_lines[0].decode("utf-8")
        print(request_line)
        # GET or POST
        method = re.match(r'(\w+)\s+/\S*',request_line).group(1)
        filename = re.match(r'\w+\s+(/\S*)',request_line).group(1)
        # print(method)
        # print(filename)
        # 要传递的内容写入一个字典中，传递给应用程序
        env = {'METHOD': method,'PATH_INFO': filename}

        response_body = self.app(env,self.set_headers)
        response = self.response_headers + '\r\n' + response_body
        # 向客户端发送response
        c.send(response.encode())
        c.close()

    def set_headers(self,status,headers):
        '''
        在app调用该函数时，希望得到
        status = "200 OK"
        headers = [
                ("Content-Type","text/plain")
                ]
        :param status:
        :param headers:
        :return:
        '''
        response_headers = "HTTP/1.1 " + status + '\r\n'
        for header in headers:
            response_headers += "%s: %s\r\n"%header#header是一个元组
        self.response_headers = response_headers

# 完成httpserver对象属性的添加和创建
def main():
    # 选择一个要使用的网站的某个app
    if len(sys.argv) < 2:
        sys.exit("""
        run the server as:
        python3 Httpserver.py FrameworkName:app
        """)
    # 获取到这个网站下的这个应用到本地
    module_name,app_name = sys.argv[1].split(":")

    sys.path.insert(1,'.')
    m = __import__(module_name)
    app = getattr(m,app_name)

    # 将该应用变为server对象的属性
    http_server = HTTPserver(app)
    http_server.bind(('0.0.0.0',8000))
    print("Listen on port 8000....")
    http_server.start()

if __name__ == '__main__':
    main()

