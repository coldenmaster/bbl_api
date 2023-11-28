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
    


# endpoint: http://bench-manager.local:8000/api/method/bbl_api.bbl_api.custom_api.api1.api1
@frappe.whitelist(allow_guest=True)
def api1(*args, **kwargs):
    print("")
    print("------------ api1(args)")
    print(args)
    print("------------ api1(kwargs)")
    print(kwargs)
    print("------------ end -------- ")
    print("")
    return "help me API" + str(kwargs)
