# Copyright (c) 2024, BBL and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils.data import add_to_date, now_datetime

from bbl_api.utils import USERS_IDS, WxcpApp, send_wx_msg_q


class ProductLength(Document):
	pass


# http://erp.v16:8000/api/method/bbl_api.bbl_api.doctype.product_length.product_length.send_product_length?up_data=123
# http://erp15.hbbbl.top:82/api/method/bbl_api.bbl_api.doctype.product_length.product_length.send_product_length
@frappe.whitelist(allow_guest=True)
def send_product_length(**data):
    data = frappe._dict(data)
    # print_green(f'{data=}')
    error_length = data.get('error_length')
    # 转成数字，并且取绝对值
    error_length = abs(float(error_length))
    if error_length > 50:
        return '长度误差大于50mm,不记录'
    
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

def daily_statistics(delta:int = 0):
    """ 
    测长短制作每日报告:仿造电表，
    日期，报告类型，产品，数量，误差+，误差-数量，误差百分比
    """
    report_type = '测长短'
    report_period = '日报'
    now_time = now_datetime()
    now_time = add_to_date(now_time, days=delta)
    # end_time = now_time.replace(hour=0, minute=0, second=0, microsecond=0)
    end_time = now_time
    start_time = add_to_date(end_time, days=-1)
    name_cnt = _get_list(start_time, end_time)
    report = {
        # 'report_type': report_type,
        # 'report_period': report_period,
        'start_time': start_time,
        'end_time': end_time,
        'name_cnt': name_cnt
    }
    rt_str = _report_str(report)
    send_wx_msg_q(rt_str, app_name=WxcpApp.PRODUCT_APP.value, user_ids=USERS_IDS.get('product_length', ''))
    # send_wx_msg_q(rt_str, app_name=WxcpApp.PRODUCT_APP.value, user_ids=USERS_IDS.get('admins', ''))
    # send_wechat_msg_admin_site(rt_str)
    # print_green(rt_str)


def _get_list(start_time, end_time):
    docs = frappe.get_list('Product Length', 
        filters={
            'creation': ['between', [start_time, end_time]],
            'error_length': ['<', 20]
        }, 
        fields=['product_name', 'length', 'error_length'])
    product_names = [d.product_name for d in docs]
    product_name_set = set(product_names)
    # print_green(product_name_set)
    name_cnt = { name: product_names.count(name) for name in product_name_set}
    name_cnt['合计'] = len(product_names)
    # _print_blue_pp(name_cnt)
    return name_cnt

def _report_str(report):
    rt_str = f'<<工件测长度日报>>\n------\n开始时间: {report.get("start_time").strftime("%Y-%m-%d %H:%M:%S")}\n结束时间: {report.get("end_time").strftime("%Y-%m-%d %H:%M:%S")}\n------'
    for name, cnt in report.get("name_cnt").items():
        rt_str += f'\n{name}: {cnt} 根'
    # rt_str += '\n------'
    return rt_str


# import bbl_api.bbl_api.doctype.product_length.product_length as pl
