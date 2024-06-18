import frappe

from bbl_api.utils import print_blue

T1_BOS = ["B22421204/0223", "B22421204/0224"]
def t1(batch_nos):
    for batch_no in batch_nos:
        frappe.db.set_value("Steel Batch", batch_no, "status", "草稿")
    frappe.db.commit()
        
def t2():

    t1(T1_BOS)
    print_blue("ok")   
        
        
        
        
if __name__ == "__main__":
    t2()