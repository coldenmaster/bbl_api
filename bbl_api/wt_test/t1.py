import frappe

from bbl_api.utils import _print_blue_pp, _print_green_pp, print_blue, print_blue_pp, print_yellow
from frappe.utils import *

T1_BOS = ["B22421204/0223", "B22421204/0224"]
def t1():

    ss = random_string(30)
    _print_blue_pp(ss)

def t2():
    print_yellow("t2")
    ss = getattr(frappe.local, "site", None) 
    print(ss)
    
    ss = frappe.local.db
    print(ss)
    

        
        
        
        
if __name__ == "__main__":
    t1()


""" DEBUG
import bbl_api.wt_test.t1 as test

bench commands 模块导入
import frappe.commands.utils as cmds

In [12]: import frappe.test_runner
In [13]: frappe.test_runner.main(doctype="Mold Test")

 """