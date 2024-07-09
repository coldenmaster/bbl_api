# Copyright (c) 2024, BBL and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

from bbl_api.utils import USERS_IDS, WxcpApp, print_red, send_wx_msg_q


class FatigueLife(Document):
	pass


# data={'data_cnt': '168', 'counter': '581380', 'frequency': '3.3', 'force_max': 119.53,
#       'force_min': 34.2, 'product_name': '153Q1572', 'semi_product': 'EQ53', 
#       'customer': '东风德纳', 'series': 'Sr123456789', 
#       'cmd': 'bbl_api.bbl_api.doctype.fatigue_life.fatigue_life.send_fatigue_life'}

# http://erp.v16:8000/api/method/bbl_api.bbl_api.doctype.fatigue_life.fatigue_life.send_fatigue_life?up_data=123
# http://erp15.hbbbl.top:82/api/method/bbl_api.bbl_api.doctype.fatigue_life.fatigue_life.send_fatigue_life
# import bbl_api.bbl_api.doctype.fatigue_life.fatigue_life as fl
@frappe.whitelist(allow_guest=True)
def send_fatigue_life(**data):
    data = frappe._dict(data)
    # print_green(f'{data=}')
    data.update({
        'doctype': 'Fatigue Life',
    })
    new_doc = frappe.get_doc(data)
    new_doc.insert(ignore_permissions=True)
    frappe.db.commit()

    msg = f'<<疲劳试验数据>>\n------\n产品名称：{new_doc.product_name}\
        \n客户:{new_doc.customer}\n试验次数：{new_doc.counter}\n试验频率：{new_doc.frequency}\
        \n最大力：{new_doc.force_max}\n最小力：{new_doc.force_min}'
    
    send_wx_msg_q(msg, app_name=WxcpApp.BI.value, user_ids=USERS_IDS.get('fatigue_life', ''))

    return new_doc.name


def alarm_demon():
    """ 定时任务，检查数据，超过一定时间未上传，报警 """

    last_doc = frappe.get_last_doc('Fatigue Life')
    last_minites = (frappe.utils.now_datetime() - last_doc.creation).total_seconds() / 60
    if (last_minites > 205):
        if not frappe.cache.get_value('fatigue_life_alarm_flag', False):
            frappe.cache.set_value('fatigue_life_alarm_flag', True)
            send_wx_msg_q(f'30分钟未收到数据，\n最后计数:{last_doc.counter}', app_name=WxcpApp.BI.value, user_ids=USERS_IDS.get('fatigue_life', ''))
            # send_wx_msg_q(f'30分钟未收到数据，\n最后计数{last_doc.counter}', app_name=WxcpApp.BI.value)
    else:
        frappe.cache.set_value('fatigue_life_alarm_flag', False)
    # print_red(f'{last_minites=}')
    # print_red(f'{ frappe.cache.get_value("fatigue_life_alarm_flag") =}')


def t1():
    frappe.cache.set_value('fatigue_life_alarm_flag', False)


def t2():
    global _alarm_flag
    print_red(f'{ frappe.cache.get_value("fatigue_life_alarm_flag", False) =}')
     
