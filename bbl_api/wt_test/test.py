import datetime
import json
import frappe
# from frappe.utils import get_fullname
import frappe.utils
from pprint import pprint
from frappe.utils.data import add_to_date, now, now_datetime
import wechat_work

from wechat_work.utils import send_str_to_admin

import bbl_api

from bbl_api.utils import *
import importlib

logger = frappe.logger("iot")


def test1():
    print_blue('bbl_api.test1.test1')

def test2(arg1, arg2):
    frappe.enqueue('myapp.mymodule.long_job', arg1=arg1, arg2=arg2)

def long_job(arg1, arg2):
    frappe.publish_realtime('msgprint', 'Starting long job...')
    # this job takes a long time to process
    frappe.publish_realtime('msgprint', 'Ending long job...')

def enqueue_long_job(arg1, arg2):
    print_blue('myapp.mymodule.long_job')
    frappe.enqueue('myapp.mymodule.long_job', arg1=arg1, arg2=arg2)
    
    
def t1():
    print_purple('bbl_api.test.t1')
    send_str_to_admin('bbl_api.test.t1')
    
    
    '''
import importlib
# from bbl_api import test
import bbl_api.test
test = bbl_api.test
test.t2()
importlib.reload(bbl_api.test) # module需要相同
# console时间长以后local报错，需要从新运行(X), 时importlib.reload(frappe)后报错,可能是丢失local指向
In [11]: importlib.reload(frappe.email.doctype.email_queue.email_queue)

    '''
    
    
def t2():
    print('bbl_api.test.t2')
    # importlib.reload(bbl_api)
    # importlib.reload(bbl_api.test)
    # print_blue(importlib.reload(bbl_api))
    print(importlib.reload(bbl_api.test))
    # print(importlib.reload(bbl_api.tasks))
    t5()
    
    
def t3():
    print_red('t3() start')
    print(frappe._("Mold"))
    # print(frappe._("Employee"))
    print_blue_kv('frappe.session.user 1: ', f'{ frappe.session.user } ')
    frappe.set_user("xiezequan@hbbbl.top")
    print_blue_kv('frappe.session.user 2: ', f'{ frappe.session.user } ')
    
    # frappe.format_value(125, dict(fieldtype='Currency'))
    from frappe.utils import format_date
    print(format_date('2023-04-01'))
    print(format_date('2023-04-01', "dd-mm-yyy"))
    print_blue_kv('frappe.form_dict: ', f'{frappe.form_dict}')
    print_blue_kv('frappe.session: ', f'{frappe.session}')
    # print_blue_kv('frappe.request', f'{frappe.request}') # wrong
    print(frappe.session.csrf_token )
    print(f"2 {frappe.session.get_fullname}")
    
    print_blue_kv('frappe.get_all: ', f'{ frappe.get_all("Mold") } ')
    print_blue_kv('frappe.get_doc("User", frappe.session.user): ', f'{ frappe.get_doc("User", frappe.session.user)} ')
    print_blue_kv('frappe.db.get_list("Mold"): ', f'{ frappe.db.get_list("Mold") } ')
    
    print_blue_kv('sql: ', f'{ frappe.db.sql(""" select name from tabMold where name like "%9%" """) }')
    frappe.cache().set_value("test_key", "test_value")
    print_blue_kv('cache: ', f'{frappe.cache().get_value("test_key")}')
    frappe.cache().hset("sales_invoice", "test_key", "test_value 2")
    print_blue_kv('cache.hset: ', f'{frappe.cache().hget("sales_invoice", "test_key")}')
    # print_blue_kv('frappe.query_builder: ', f'{frappe.qb.from_("Employee").select("*").run()}') #ok
    print_blue_kv('msgprint: ', f'{frappe.msgprint("wtt ok", wide=True)}')
    # print_blue_kv('hooks: ', f'{frappe.get_hooks()}') # too much
    print_blue_kv('frappe.user: ', f'{frappe.utils.get_fullname()}')
    print_blue_kv('frappe.get_user(): ', f'{frappe.get_user()}')
    # print_blue_kv('log_error: ', f'{frappe.log_error("wtt abc")}') #ok
   
    print_blue_kv('frappe.sendmail: ', f"{ frappe.sendmail(now=True, recipients=['15894368@qq.com'], sender='sender@example.com', subject='t3', message='<p>Hello</p>') }")
    
    
    print_red('over 7')
    
    
def t4():
    print_red('t4() start')
    print_blue_kv('frappe.session.user 1: ', f'{ frappe.session.user } ')
    # frappe.set_user("Administrator")
    # frappe.sendmail(now=True, recipients=['15894368@qq.com'], sender='sender@example.com', subject='t4 True 大傻逼', message='<p>Hello dsb</p>')
    frappe.sendmail(now=False, queue_separately=True, recipients=['15894368@qq.com'], sender='sender@example.com', subject='t4 False 大傻逼', message='<p>Hello dsb</p>')
    print_red('t4 over')
    
def t5():
    print('t5() start')
    t7()
    # t8()
    
    print('t5() end')
    
def t6():
    # li = frappe.db.get_list('User', filters={'name': 'Administrator'}, fields=['name', 'email', 'full_name'])
    # li = frappe.db.get_list('User', fields=['name', 'email', 'full_name'])
    # li = frappe.db.get_list('Employee',  fields=['name', 'first_name',] )
    # li = frappe.db.get_list('Employee', pluck = 'first_name')
    # li = frappe.db.get_list('Employee',
    #                         filters =  {
    #                             'first_name': ['like', '%王%'],
    #                         },
    #                         order_by='modified asc',
    #                         # start = 5,
    #                         # page_length = 3,
    #                         # fields=['name', 'first_name',],
    #                         # distinct = True,
    #                         # as_list = True,
    #                         pluck = 'first_name'
    #                         )
    # print_blue_pp(li)
    # print_green(f'list cnt: {len(li)}')
    # t7()
    pass

def t7():
    # now = datetime.datetime.now()
    # start_time = now + datetime.timedelta(days=-32)
    # while (start_time < now):
    #     date = start_time.strftime('%Y-%m-%d')
    #     print(date)
    #     em_perday_test(start_time)
    #     start_time += datetime.timedelta(days=1)

    
    # em_perday()
    # em_permonth()
    pass
    

def t8():
    #test
    print(frappe.get_site_path())
    print(dir(frappe.local))
    print(frappe.local.site)
    print(frappe.get_conf)
    pass


# def em_perday_test(date):
#     # 计算时间区间，可以使用此程序运行时间，或者使用固定时间
#     report_type = '日报'
#     now = date
#     end_time = now.replace(hour=0, minute=0, second=0, microsecond=0)
#     start_time = end_time + datetime.timedelta(days=-1)
#     print_red(f"perday start_time: {start_time}")
#     print_red(f"perday end_time: {end_time}")
#     # 获取电表列表
#     doc = 'Elec Meter RT'
#     li = em_list(doc, start_time, end_time)
    
#     for em_name in li:
#         em_calc(doc, report_type, em_name, start_time, end_time)

