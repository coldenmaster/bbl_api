from enum import Enum
import time
from datetime import datetime

import frappe
from frappe.utils.data import DATE_FORMAT, now
import wechat_work
import wechat_work.utils

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
    
def print_obj(obj):
    # print_blue_pp(f"{obj=} \n {obj.__dict__}")
    print_blue_pp(obj.__dict__)

def print_clear(msg):
    pass

from pprint import pprint, pformat

def print_blue_pp(msg):
    if frappe.conf.wt_dev:
        _print_blue_pp(msg)

def _print_blue_pp(msg):
    msg = str(pformat(msg))
    print(f"{Color.BLUE}{msg}{Color.RESET}")

def print_green_pp(msg):
    if frappe.conf.wt_dev:
        print(f"{Color.GREEN}{str(pformat(msg))}\n{Color.RESET}")
    
def _print_green_pp(msg):
    print(f"{Color.GREEN}{str(pformat(msg))}\n{Color.RESET}")

    
# 微信发送信息相关
class WxcpGroupTag(Enum):
    MAINTAIN = 1
    TEMPRATURE = 2
    NET_MANAGE = 5
    ELEC_METER = 6
    QUALITY = 7
    RAW_MATERIAL = 8
    TEST_TAG = 9
    PRODUCT_QTY = 10
    
class WxcpApp(Enum):
    ELEC_METER = 'EM_APP'
    PRODUCT_APP = 'PRODUCT_APP'
    TEMPRATURE = 'TEMP_APP'
    QUALITY = 'TEMP_APP'
    MAINTAIN = '维修APP'
    BI = '数据可视化'
    TEST = 'TEST_APP'
    BBL_CLOUD = 'BBL云服务'
    RAW_MATERIAL = '钢棒管理'
    FORGE_APP = '锻造APP'
    GAS_ALARM = '燃气报警'
    # NET_MANAGE = 'NET_APP'
    
USERS_IDS = {
    'fatigue_life': ['wangtao', 'mayanbing', 'shijie','xingxing', 'buyiyangdehuo',],
    'product_length': ['wangtao', 'mayanbing', 'shijie','yizhiyu', 'weili',],
    'product_scan_code': ['wangtao', 'mayanbing', 'shijie', 'cp'],
    'admins': ['wangtao', ],
    'other': ['cp', 'shicong', '','',]
}

def msg_end():
    site = frappe.local.site if frappe.local.site != 'frontend' else ''
    return f'\n------\n{now()}\n{site}'

# 送到 管理员
def send_wechat_msg_admin_site(msg):
    msg = msg + msg_end()
    wechat_work.utils.send_str_to_admin(msg)

# 送到 TEMP_APP 中频测温
def send_wechat_msg_temp_app(msg):
    msg = msg + msg_end()
    wechat_work.utils.send_str_to_wework(msg, app_name='TEMP_APP', tag_ids='2')

# 送到 EM_APP 电表数据
def send_wechat_msg_em_app(msg):
    msg = msg + msg_end()
    wechat_work.utils.send_str_to_wework(msg, app_name='EM_APP', tag_ids='6')

# 送到 PRODUCT_APP 产品数量
def send_wechat_msg_product_app(msg):
    msg = msg + msg_end()
    wechat_work.utils.send_str_to_wework(msg, app_name='PRODUCT_APP', tag_ids=WxcpGroupTag.PRODUCT_QTY.value)


# # todo 队列发送 
def send_wx_admin_q(msg):
    send_wx_msg_q(msg)
    
def send_wechat_msg_temp_queue(msg):
    send_wx_msg_q(msg, app_name='TEMP_APP', tag_ids='2')
      
def send_wechat_msg_product_queue(msg):
    send_wx_msg_q(msg, app_name='PRODUCT_APP', tag_ids=WxcpGroupTag.PRODUCT_QTY.value)

# todo 统一发送 API
def send_wx_msg_q(msg, now=False, app_name='TEST_APP', tag_ids='', party_ids='', user_ids='wangtao'):
    # print("统一发送 API")
    msg = msg + msg_end()
    frappe.enqueue(wechat_work.utils.send_str_to_wework, queue='short', now=now, msg = msg, 
                   app_name=app_name, tag_ids=tag_ids, party_ids=party_ids, user_ids=user_ids)













# 其它工具

_TIME_FORMAT = "%H:%M:%S"
def bbl_now() -> str:
    # return now_datetime().strftime(DATE_FORMAT + _TIME_FORMAT)
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S") # 脱离 frappe

# frappe.utils 内已经有了(first_name + last_name), 我这个是直接取full_name
def get_fullname(user_id:str = None):
    if not user_id:
        user_id = frappe.session.user
    return frappe.db.get_value('User', user_id, ['full_name'])











# todo DEBUG
@frappe.whitelist(allow_guest=True)
@timer
# http://127.0.0.1:8000/api/method/wechat_work.utils.t1&msg=sb250
def t1(*args, **kwargs):
    print("\n----------- wechat_work")
    msg = f"t1: { kwargs.get('msg', '喵喵喵') }"
    wechat_work.utils.send_str_to_wework(msg, "维修记录")
    return msg



# """ 控制台测试方法
# import bbl_app.utils as utils
# sb.make_out_entry(**sb.k3)
# docs = frappe.get_all("Steel Batch")
# """