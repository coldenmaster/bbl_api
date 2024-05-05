import time

import frappe
from frappe.utils.data import DATE_FORMAT, now, now_datetime
import wechat_work

import bbl_api


def timer(func):
    def func_in():
        startTime = time.time()
        rt = func()
        print("耗时: %.03f 秒" % (time.time() - startTime))
        return rt
    return func_in

def progress_bar(total):
    for i in range(total + 1):
        progress = i / total * 100
        print(f"\rProgress: [{('#' * int(progress / 10)).ljust(10)}] {progress:.2f}%", end="")
        time.sleep(0.1)

class Color:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    GRAY = '\033[90m'
    WHITE = '\033[97m'
    RESET = '\033[0m'

def print_red(msg):
    print(f"{Color.RED}{msg}{Color.RESET}")

def print_white(msg):
    print(f"{Color.WHITE}{msg}{Color.RESET}")

def print_gray(msg):
    print(f"{Color.GRAY}{msg}{Color.RESET}")

def print_cyan(msg):
    print(f"{Color.CYAN}{msg}{Color.RESET}")

def print_purple(msg):
    print(f"{Color.PURPLE}{msg}{Color.RESET}")

def print_yellow(msg):
    print(f"{Color.YELLOW}{msg}{Color.RESET}")

def print_blue(msg):
    print(f"{Color.BLUE}{msg}{Color.RESET}")
    
def print_blue_kv(key, msg):
    print(f"{Color.BLUE}{key}{Color.RESET}{msg}")

def print_green(msg):
    print(f"{Color.GREEN}{msg}{Color.RESET}")
    
def print_clear(msg):
    pass

from pprint import pprint, pformat

def print_blue_pp(msg):
    msg = str(pformat(msg))
    # print(f"{Color.BLUE}{pformat(msg)}{Color.RESET}")
    print(f"{Color.BLUE}{msg}{Color.RESET}")

def print_green_pp(msg):
    print(f"{Color.GREEN}{str(pformat(msg))}\n{Color.RESET}")
    
    
# 微信发送信息相关
def send_wechat_msg_admin_site(msg):
    msg = f'[{frappe.local.site}]\n[{now()}]\n{msg}'
    wechat_work.utils.send_str_to_admin(msg)

def send_wechat_msg_temp_app(msg):
    msg = f'[{frappe.local.site}]\n[{now()}]\n{msg}'
    wechat_work.utils.send_str_to_wework(msg, app_name='TEMP_APP', tag_ids='2')

def send_wechat_msg_em_app(msg):
    msg = f'[{frappe.local.site}]\n[{now()}]\n{msg}'
    wechat_work.utils.send_str_to_wework(msg, app_name='EM_APP', tag_ids='6')

def send_wechat_msg_product_app(msg):
    msg = f'[{frappe.local.site}]\n[{now()}]\n{msg}'
    wechat_work.utils.send_str_to_wework(msg, app_name='PRODUCT_APP', tag_ids='6')

def send_wechat_msg_admin_site_queue(msg):
    frappe.enqueue(bbl_api.utils.send_wechat_msg_admin_site, queue='short', now=True, msg = msg)
    
def send_wechat_msg_temp_queue(msg):
    frappe.enqueue(bbl_api.utils.send_wechat_msg_temp_app, queue='short', now=True, msg = msg)
      
def send_wechat_msg_product_queue(msg):
    frappe.enqueue(bbl_api.utils.send_wechat_msg_product_app, queue='short', now=True, msg = msg)
   

# 其它工具

_TIME_FORMAT = "%H:%M:%S"
def bbl_now() -> str:
    return now_datetime().strftime(DATE_FORMAT + _TIME_FORMAT)

# frappe.utils 内已经有了(first_name + last_name), 我这个是直接取full_name
def get_fullname(user_id:str = None):
    if not user_id:
        user_id = frappe.session.user
    return frappe.db.get_value('User', user_id, ['full_name'])
