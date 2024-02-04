import frappe

from bbl_api.utils import print_blue

def test1():
    print_blue('bbl_api.test1.t1')

def test2(arg1, arg2):
    frappe.enqueue('myapp.mymodule.long_job', arg1=arg1, arg2=arg2)

def long_job(arg1, arg2):
    frappe.publish_realtime('msgprint', 'Starting long job...')
    # this job takes a long time to process
    frappe.publish_realtime('msgprint', 'Ending long job...')

def enqueue_long_job(arg1, arg2):
    print_blue('myapp.mymodule.long_job')
    frappe.enqueue('myapp.mymodule.long_job', arg1=arg1, arg2=arg2)