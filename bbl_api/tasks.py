
from bbl_app.machine_shop.doctype.product_scan.product_scan import product_qrcode_daily_statistics
from bbl_app.raw_material_manage.doctype.raw_balance.raw_balance import make_raw_material_balance
from bbl_api.api01.em_parse import em_perday, em_permonth
from bbl_api.api01.zpl import zpl_perday
from bbl_api.bbl_api.doctype.fatigue_life.fatigue_life import alarm_demon
from bbl_api.bbl_api.doctype.product_length.product_length import daily_statistics
from bbl_api.utils import send_wechat_msg_admin_site
from frappe.utils import now

# 根据site_config 配置定时任务tick
def all():
    # msg = f"scheduler: {now()} All"
    # send_wechat_msg_admin_site(msg)
    pass
    
    
def hourly():
    # msg = f"scheduler hourly(网站每小时tick):"
    # send_wechat_msg_admin_site(msg)
    pass
        
def hourly_long():
    # no this
    # msg = f"scheduler: {now()} hourly"
    # send_str_to_admin(msg)
    pass
    
def daily():
    # em_perday()
    # msg = f"scheduler daily: {now()} "
    # send_wechat_msg_admin_site(msg)
    em_perday()
    pass
        
def daily_long():
    # msg = f"scheduler daily_long(处理每日例行任务):"
    # send_wechat_msg_admin_site(msg)
    pass
    
def daily_00_10m():
    now2 = now()

def daily_08_10m():
    msg = f"daily_08_10m: {now()}"
    send_wechat_msg_admin_site(msg)
    zpl_perday()


def daily_18_00m():
    msg = f"daily_08_10m: {now()}"
    send_wechat_msg_admin_site(msg)
    daily_statistics()
    product_qrcode_daily_statistics()
    
def weekly():
    msg = f"scheduler weekly: {now()}"
    send_wechat_msg_admin_site(msg)
    
def weekly_long():
    msg = f"scheduler weekly: {now()}"
    send_wechat_msg_admin_site(msg)
    
def monthly():
    # em_permonth()
    msg = f"scheduler monthly: {now()} "
    # send_wechat_msg_admin_site(msg)
        
def monthly_long():
    msg = f"scheduler long: {now()} "
    make_raw_material_balance()
    # send_wechat_msg_admin_site(msg)

def monthly_1_00_30m():
    msg = f"monthly_1_00_30m: {now()}"
    send_wechat_msg_admin_site(msg)
    em_permonth()

def minute_per5():
    # msg = f"scheduler: {now()} minute_per5"
    # send_wechat_msg_admin_site(msg)
    alarm_demon()
    pass
        
def minute_per30():
    # msg = f"scheduler: {now()} minute_per30"
    # send_wechat_msg_admin_site(msg)
    pass
            
def minute_30():
    # msg = f"scheduler: {now()} minute_30"
    # send_wechat_msg_admin_site(msg)
    pass
    
def minutely():
    # msg = f"scheduler minutely: {now()}"
    # send_wechat_msg_admin_site(msg)
    pass
    
def annual():
    msg = f"scheduler annual: {now()} "
    send_wechat_msg_admin_site(msg)

def yearly():
    msg = f"scheduler yearly: {now()}"
    send_wechat_msg_admin_site(msg)

""" debug
import bbl_api.tasks as tasks

 """
    
