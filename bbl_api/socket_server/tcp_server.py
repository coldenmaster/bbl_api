from datetime import datetime
from multiprocessing import Process
import socket
import socketserver

from bbl_api.utils import print_green, print_purple
 
class MyTCPHandler(socketserver.StreamRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    
    def handle(self):
        time_out = 30
        print(f"MyTCPHandler handle: set {time_out = }s")
        self.request.settimeout(time_out)
        # self.request is the TCP socket connected to the client
        dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            self.data = self.request.recv(1024).strip()
            print_purple("[{}] [{}:{}] wrote:".format(dt, self.client_address[0], self.client_address[1]))
            print_green(self.data)
            # just send back the same data, but upper-cased
            # self.request.sendall(self.data.upper())
            # self.request.sendall(b"self.data")
            self.request.sendall(self.data)
        except Exception as e:
            print_purple("[{}] [{}:{}]连接超时:{}".format(dt, self.client_address[0], self.client_address[1],e))
            self.finish()

# class MyTCPServer(socketserver.ThreadingTCPServer):
#     pass

# class MyTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
#     pass


def parse_data(data):
    print_purple(f"parse_data:{data = }")
    

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('localhost', port))
            return False
        except:
            return True

def run_tcp_server(port):
    print_purple(f"run_tcp_server")
    HOST, PORT = "0.0.0.0", port

    socketserver.TCPServer.allow_reuse_address = True

    # with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
    with socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        # server.allow_reuse_address = True # 设置为True以允许重用地址
        server.serve_forever()

def start_tcp_server(port):
    if is_port_in_use(port):
        print_purple(f"{port} 端口被占用")
        return
    print_purple(f"打开新进程 for tcp")
    run_tcp_server(port)
    # 在新进程中开启tcp server
    # p = Process(target=run_tcp_server, args=(port,))
    # p.start()


""" 调试
 # 查看端口占用情况
 sudo netstat -anp | grep 8002 


 """