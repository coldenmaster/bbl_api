
import wechat_work
from wechat_work.utils import send_str_to_admin
from bbl_api.test import em_perday
from bbl_api.utils import print_purple
from frappe.utils import now

def all():
    msg = f"scheduler: {now()} All"
    send_wechat_msg_here(msg)
    
    
def hourly():
    msg = f"scheduler: {now()} hourly"
    send_str_to_admin(msg)
    
def daily():
    em_perday()
    msg = f"scheduler: {now()} daily"
    send_wechat_msg_here(msg)
    
def weekly():
    msg = f"scheduler: {now()} weekly"
    send_wechat_msg_here(msg)
    
def monthly():
    msg = f"scheduler: {now()} monthly"
    send_wechat_msg_here(msg)
    
def minute_5():
    msg = f"scheduler: {now()} minute_5"
    send_wechat_msg_here(msg)
    
def annual():
    msg = f"scheduler: {now()} annual"
    send_wechat_msg_here(msg)

def send_wechat_msg_here(msg):
    wechat_work.utils.send_str_to_admin(msg)
    pass

    
