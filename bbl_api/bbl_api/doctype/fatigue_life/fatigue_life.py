# Copyright (c) 2024, BBL and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

from bbl_api.utils import print_green


class FatigueLife(Document):
	pass


# data={'data_cnt': '168', 'counter': '581380', 'frequency': '3.3', 'force_max': 119.53,
#       'force_min': 34.2, 'product_name': '153Q1572', 'semi_product': 'EQ53', 
#       'customer': '东风德纳', 'serial_number': 'Sr123456789', 
#       'cmd': 'bbl_api.bbl_api.doctype.fatigue_life.fatigue_life.send_fatigue_life'}

# http://erp.v16:8000/api/method/bbl_api.bbl_api.doctype.fatigue_life.fatigue_life.send_fatigue_life?up_data=123
# http://erp15.hbbbl.top:82/api/method/bbl_api.bbl_api.doctype.fatigue_life.fatigue_life.send_fatigue_life
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
    return new_doc.name
