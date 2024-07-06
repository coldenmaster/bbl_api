# Copyright (c) 2024, BBL and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

from bbl_api.utils import USERS_IDS, WxcpApp, send_wechat_msg_temp_queue, send_wx_msg_q


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

    msg = f'<<疲劳试验数据上传成功>>\n------\n产品名称：{new_doc.product_name}\
        \n客户:{new_doc.customer}\n试验次数：{new_doc.counter}\n试验频率：{new_doc.frequency}\
        \n最大力：{new_doc.force_max}\n最小力：{new_doc.force_min}'
    # send_wechat_msg_temp_queue(msg)
    send_wx_msg_q(msg, app_name=WxcpApp.BI.value, user_ids=USERS_IDS.get('fatigue_life', ''))

    return new_doc.name
