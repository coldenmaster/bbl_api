import frappe

# todo 没用使用
# 准备在此api下接收旧的esp上传数据，进行测试。
# endpoint: http://127.0.0.1:8000/api/method/bbl_api.api.t1
# wtCnt = 0
# @frappe.whitelist(allow_guest=True)
# def t1(*args, **kwargs):
#     global wtCnt
#     wtCnt = wtCnt + 1
#     print(f"\n--- short api t1(args) cnt: {wtCnt}")
#     print(f"---kwargs is {kwargs}\n")
#     return f"stapi.t1() response({wtCnt}): {str(kwargs)}"

# # endpoint: http://127.0.0.1:8000/api/method/bbl_api.api.t1
# @frappe.whitelist(allow_guest=True)
# def t2(*args, **kwargs):
#     global wtCnt
#     print(f"\n--- short api t2(args) cnt: {wtCnt}")
#     print(f"---kwargs is {kwargs}\n")
#     return f"stapi.t1() response({wtCnt}): {str(kwargs)}"
