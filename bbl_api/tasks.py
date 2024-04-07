
from bbl_api.api01.em_parse import em_perday, em_permonth
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
        
def hourly_long():
    # msg = f"scheduler: {now()} hourly"
    # send_str_to_admin(msg)
    pass
    
def daily():
    # em_perday()
    msg = f"scheduler daily: {now()} "
    send_wechat_msg_here(msg)
    pass
        
def daily_long():
    msg = f"scheduler daily_long: {now()}"
    send_wechat_msg_here(msg)
    em_perday()
    
def daily_00_10m():
    now2 = now()
    # msg = f"daily_00_10m: {now2}"
    # print(msg)
    # send_wechat_msg_here(msg)
    
def weekly():
    msg = f"scheduler weekly: {now()}"
    send_wechat_msg_here(msg)
    
def weekly_long():
    msg = f"scheduler weekly: {now()}"
    send_wechat_msg_here(msg)
    
def monthly():
    # em_permonth()
    msg = f"scheduler monthly: {now()} "
    send_wechat_msg_here(msg)
        
def monthly_long():
    msg = f"scheduler long: {now()} "
    send_wechat_msg_here(msg)
    em_permonth()
    
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
    
def minutely():
    # msg = f"scheduler minutely: {now()}"
    # send_wechat_msg_here(msg)
    pass
    
def annual():
    msg = f"scheduler annual: {now()} "
    send_wechat_msg_here(msg)

def yearly():
    msg = f"scheduler yearly: {now()}"
    send_wechat_msg_here(msg)


    
