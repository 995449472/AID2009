import re
from socket import *
from select import select


class WebServer:
    # * 表示后面的参数必须以关键字的方式传参
    def __init__(self, *, host="0.0.0.0", port=80, html=None):
        self.host = host
        self.port = port
        self.html = html
        # 准备工作
        self.create_sock()
        self.bind()
        self.rlist = []  # 初始,监听套接字
        self.wlist = []
        self.xlist = []

    # 创建套接字
    def create_sock(self):
        self.sock = socket()
        self.sock.setblocking(False)

    def bind(self):
        self.address = (self.host, self.port)
        self.sock.bind(self.address)

    def connect(self, sockfd):
        connfd, addr = sockfd.accept()
        print(addr, "已连接")
        connfd.setblocking(False)
        # 每链接一个客户端就多监控一个
        self.rlist.append(connfd)


    def send_html(self, connfd, info):
        if info == "/":
            filename = self.html + "/index.html"
        else:
            filename = self.html + info
        try:
            file = open(filename, "rb")
        except:
            # 请求的网页不存在:
            with open(self.html+"/404.html", "rb") as f:
                data = f.read()
            response = "HTTP/1.1 404 Not Found\r\n"
            response += "Content-Type:text/html\r\n"
            response += "\r\n"
            response = response.encode() + data
        else:
            data = file.read()
            response = "HTTP/1.1 200 OK\r\n"
            response += "Content-Type:text/html\r\n"
            response += "\r\n"
            response = response.encode() + data
        finally:
            connfd.send(response)



    def handle(self, connfd):
        # 接收请求
        request = connfd.recv(1024).decode()
        print(request)
        # 提取请求内容
        pattern = r"[A-Z]+\s+(?P<info>/\S*)"
        result = re.match(pattern, request)  # match/none
        if request:
            info = result.group("info")
            self.send_html(connfd, info)
        else:
            # 函数结束
            return
        print(info)

    # 启动网络服务 --> IO并发模型
    def start(self):
        self.sock.listen(5)
        self.rlist.append(self.sock)
        while True:
            rs, ws, xs = select(self.rlist, self.wlist, self.xlist)
            # 接收链接
            for r in rs:
                if r is self.sock:
                    self.connect(r)
                else:
                    # 某个浏览器发送http请求
                    try:
                        self.handle(r)
                    except:
                        pass
                    finally:
                        r.close()
                        self.rlist.remove(r)




if __name__ == '__main__':
    # 使用者怎么用
    # 传参->地址,网页
    httpd = WebServer(port=8085, html="./static")
    # 启动服务
    httpd.start()
