'''
-*- coding: utf-8 -*-
@Author  : LiZhichao
@Time    : 2019/8/17 15:51
@Software: PyCharm
@File    : HttpServer1.py
'''
"""
实现多线程并发
将HttpServer的创建部分封装成类
用不同的后端程序处理不同的请求
可以简单的显示静态页面
"""
import sys
from socket import *
from threading import *

#全局变量
Addr = ('0.0.0.0',8000)
#存静态网页
static_root = "./static"
#存放Python处理模块
handler_root = "./handler"

#httpserver类
class HTTPServer(object):
    def __init__(self,addr):
        self.addr = addr
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
        self.sockfd.bind(Addr)
        self.sockfd.listen(5)
        self.serveName = '127.0.0.1'
        self.servePort = 8000

    #服务端启动函数：接收客户端请求，创建新的线程
    def serveForever(self):
        while True:
            self.connfd,self.clientAddr = self.sockfd.accept()
            clientThread = Thread(target=self.handleRequest)
            clientThread.start()

    def setApp(self,application):
        self.application = application

    def handleRequest(self):
        #接收request请求
        self.recvData = self.connfd.recv(2048)
        requestHeaders = self.recvData.splitlines()
        for line in requestHeaders:
            print(line)
        # 获取到从浏览器输入的具体请求
        getRequest = str(requestHeaders[0]).split(' ')[1]
        if getRequest[-3:] != '.py':
            if getRequest == '/':
                getFilename = static_root + "/index.html"
            else:
                getFilename = static_root + getRequest

            try:
                f = open(getFilename)
            except:
                responseHeaders = "HTTP/1.1 404 not found"
                responseHeaders += '\r\n'
                responseBody = "=====sorry,file not found======"
            else:
                responseHeaders = "HTTP/1.1 200 OK\r\n"
                responseHeaders += '\r\n'
                responseBody = f.read()
            finally:
                response = responseHeaders + responseBody
                self.connfd.send(response.encode())
        else:
            # 需要的环境变量
            env = {}
            bodyContent = self.application(env,self.startResponse)
            response = "HTTP/1.1 {}\r\n".format(self.header_set[0])
            for header in self.header_set[1:]:
                response += "{0}:{1}\r\n".format(*header)
            response += '\r\n'
            response += bodyContent
            self.connfd.send(response.encode())
        self.connfd.close()

    def startResponse(self,status,response_headlers):
        serverHeaders = [
            ('Data','2019-8-18'),
            ('Server','HtTPServer 1.0'),
        ]
        self.header_set = [status,response_headlers +serverHeaders]

#控制服务器启动
def main():
    #启动时直接告知使用哪个模块哪个函数处理请求
    #python3 HttpServer1.py module app
    if len(sys.argv) < 3:
        sys.exit("请选择一个模块和应用")

    #将handler文件夹加入搜索路径
    sys.path.insert(0,handler_root)
    #导入module模块
    m = __import__(sys.argv[1])
    #获取module下的app 赋值给一个变量
    application = getattr(m,sys.argv[2])

    httpd = HTTPServer(Addr)
    httpd.setApp(application)
    print("Serving HTTP on port 8000")
    httpd.serveForever()

if __name__ == '__main__':
    main()