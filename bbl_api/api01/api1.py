import frappe
import os

# @frappe.whitelist()
@frappe.whitelist(allow_guest=True)
def action1(*args, **kwargs):
    print("-------------WTTAPI Action1 On")
    # print(kwargs)
    # values = {'company': 'Frappe Technologies Inc'}
    # data = frappe.db.sql("""
    #     SELECT
    #         acc.account_number
    #         gl.debit
    #         gl.credit
    #     FROM `tabGL Entry` gl
    #         LEFT JOIN `tabAccount` acc
    #         ON gl.account = acc.name
    #     WHERE gl.company = %(company)s
    # """, values=values, as_dict=0)
    print(os.getcwd())
    print("-------------WTTAPI Action1 End")
    return "help me action1() 2"
    


# endpoint: http://127.0.0.1:8000/api/method/bbl_api.api01.api1.api1
@frappe.whitelist(allow_guest=True)
def api1(*args, **kwargs):
    print("")
    print("------------api01 阿皮 api1(args)")
    print(args)
    print("------------ api1(kwargs)")
    print(kwargs)
    print("------------ end -------- ")
    print("")
    return "api01 help me API" + str(kwargs)

# endpoint: http://127.0.0.1:8000/api/method/bbl_api.api01.api1.api2
@frappe.whitelist(allow_guest=True)
def api2(*args, **kwargs):
    print("")
    print("------------api02 阿皮 api1(args)")
    print(args)
    print("------------ api1(kwargs)")
    print(kwargs)
    print("------------ end -------- ")
    print("")
    return "api02 help me API" + str(kwargs)


# endpoint: http://127.0.0.1:8000/api/method/bbl_api.api01.api1.espxx
@frappe.whitelist(allow_guest=True)
def espxx(*args, **kwargs):
    print("")
    print("------------I'm espxx (args) is")
    print(args)
    print("------------ (kwargs) is")
    print(kwargs)
    print("------------ end -------- ")
    print("")
    return "esp API rcv: " + str(kwargs)
