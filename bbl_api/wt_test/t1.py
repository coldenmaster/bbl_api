import frappe

from bbl_api.utils import _print_blue_pp, _print_green_pp, print_blue, print_blue_pp
from frappe.utils import *

T1_BOS = ["B22421204/0223", "B22421204/0224"]
def t1():

    ss = get_formatted_email('gaoxuesong@hbbbl.top')
    _print_blue_pp(ss)


    ss = random_string(30)
    _print_blue_pp(ss)
        
        

    ss = get_gravatar_url('gaoxuesong@hbbbl.top')
    _print_blue_pp(ss)
        
        
    tt = 'sdf,sdf<dsadf125 5d2f5> ds'

    ss = get_file_timestamp('.\apps')
    _print_blue_pp(ss)
        
    ss = ''
    _print_blue_pp(ss)
        
        

    ss = get_site_info()
    _print_blue_pp(ss)
        
        

    ss = get_formatted_email('gaoxuesong@hbbbl.top')
    _print_blue_pp(ss)
        
        
        
        
if __name__ == "__main__":
    t1()


""" DEBUG
import bbl_api.wt_test.t1 as test

 """