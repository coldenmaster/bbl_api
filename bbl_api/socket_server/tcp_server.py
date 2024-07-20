from datetime import datetime
import json
import socket
import socketserver
import struct
import traceback

import requests

from bbl_api.utils import _print_green_pp, print_blue, print_purple
 
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
            # print_green(self.data)
            parse_data(self.data)
            # just send back the same data, but upper-cased
            # self.request.sendall(self.data.upper())
            self.request.sendall(self.data)
            # self.request.sendall(b'tcp recv ok!')
        except Exception as e:
            print_purple("[{}] [{}:{}]连接超时:{}".format(dt, self.client_address[0], self.client_address[1],e))
            self.finish()

# class MyTCPServer(socketserver.ThreadingTCPServer):
#     pass

# class MyTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
#     pass


def parse_data(data):
    """ 使用struct 解析 data"""

    print_purple(f"tcp接收数据:\n{data = }")
    parse_product_length(data)


def parse_product_length(data):
    print_blue(f'{len(data) = }, if len < 100, return')
    if len(data) < 100:
        return
    try:
        ss = struct.unpack('16s', data[0:16])[0].decode('utf-8').strip()
        # print_blue(f'1{  ss=}')
        product_name = ''
        for i in range(0, len(ss), 2):
            product_name += ss[i+1] + ss[i]
        product_name = product_name.replace('\x00', '')

        idx = 16; data_li = []
        for _ in range(8):
            if idx + 4 > len(data):
                break
            num = struct.unpack('!I', data[idx+2:idx+4]+data[idx:idx+2] )[0]
            data_li.append(num)
            # print_blue(f"{idx} -- {num}")
            idx += 4
        # print_blue(f"{data_li = }")

        send_product_length({
            "product_name": product_name,
            "sample_length": data_li[0]/1000,
            "standard_length": data_li[1]/1000,
            "standard_error_plus": data_li[2]/1000,
            "standard_error_minus": data_li[3]/1000,
            "product_length": data_li[4]/1000,
            "total_production": data_li[5],
            "batch_production": data_li[6],
            "error_length": (data_li[4]-data_li[1])/1000,
        })
    except Exception as e:
        traceback.print_exc()
        print(f"parse_product_length Exception:{e = }")

def send_product_length(data):
    # print_green(f"send_product_length:{data = }")
    # _print_green_pp(data)
    # url = "127.0.0.1:8000/api/method/bbl_api.api.socket_server.send_fatigue_life_data"
    # url = "http://127.0.0.1:8000/api/method/frappe.ping"
    # url = "http://erp.v16:8000/api/method/bbl_api.bbl_api.doctype.product_length.product_length.send_product_length"
    url = "http://erp15.hbbbl.top:82/api/method/bbl_api.bbl_api.doctype.product_length.product_length.send_product_length"
    
    json_data = json.dumps(data)
    response = requests.post(url, data=json_data, headers={'Content-Type': 'application/json'})
    # print_blue(f"send_product_length:{response = }")
    print_blue(f"send_product_length ok, response:{response.json() = }")
    

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


""" DEBUG
 # 查看端口占用情况
 sudo netstat -anp | grep 8002 


 """