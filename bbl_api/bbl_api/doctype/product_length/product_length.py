# Copyright (c) 2024, BBL and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

from bbl_api.utils import print_green


class ProductLength(Document):
	pass


# http://erp.v16:8000/api/method/bbl_api.bbl_api.doctype.product_length.product_length.send_product_length?up_data=123
# http://erp15.hbbbl.top:82/api/method/bbl_api.bbl_api.doctype.product_length.product_length.send_product_length
# import bbl_api.bbl_api.doctype.product_length.product_length as fl
@frappe.whitelist(allow_guest=True)
def send_product_length(**data):
    data = frappe._dict(data)
    print_green(f'{data=}')
    data.update({
        'doctype': 'Product Length',
    })
    new_doc = frappe.get_doc(data)
    new_doc.insert(ignore_permissions=True)
    frappe.db.commit()

    # msg = f'<<疲劳试验数据>>\n------\n产品名称：{new_doc.product_name}\
    #     \n客户:{new_doc.customer}\n试验次数：{new_doc.counter}\n试验频率：{new_doc.frequency}\
    #     \n最大力：{new_doc.force_max}\n最小力：{new_doc.force_min}'
    
    # send_wx_msg_q(msg, app_name=WxcpApp.BI.value, user_ids=USERS_IDS.get('product_length', ''))

    return new_doc.name
