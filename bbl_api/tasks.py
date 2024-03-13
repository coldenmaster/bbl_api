
import datetime
import frappe
from bbl_api.test import em_perday, em_permonth
from bbl_api.utils import send_wechat_msg_here
from frappe.utils import now

def all():
    # msg = f"scheduler: {now()} All"
    # send_wechat_msg_here(msg)
    pass
    
    
def hourly():
    # msg = f"scheduler: {now()} hourly"
    # send_str_to_admin(msg)
    pass
    
def daily():
    em_perday()
    msg = f"scheduler: {now()} daily"
    send_wechat_msg_here(msg)
    
def daily_00_10m():
    em_perday()
    now1 = datetime.datetime.now()
    now2 = now()
    msg = f"daily_00_10m: {now1}, {now2}"
    print(msg)
    send_wechat_msg_here(msg)
    
def weekly():
    msg = f"scheduler: {now()} weekly"
    send_wechat_msg_here(msg)
    
def monthly():
    em_permonth()
    msg = f"scheduler: {now()} monthly"
    send_wechat_msg_here(msg)
    
def minute_per5():
    # msg = f"scheduler: {now()} minute_per5"
    # send_wechat_msg_here(msg)
    pass
        
def minute_per30():
    # msg = f"scheduler: {now()} minute_per30"
    # send_wechat_msg_here(msg)
    pass
            
def minute_30():
    msg = f"scheduler: {now()} minute_30"
    send_wechat_msg_here(msg)
    
def annual():
    msg = f"scheduler: {now()} annual"
    send_wechat_msg_here(msg)


    
