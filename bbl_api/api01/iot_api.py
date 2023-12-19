import frappe
import os
import json



# endpoint: http://127.0.0.1:8000/api/method/bbl_api.api01.iot_api.upStat
# http://127.0.0.1:8000/api/method/bbl_api.api01.iot_api.upStat?espId=espGas2&wifiSsid=HIKbs3&mac=F4:CF:A2:F7:5D:4C&wifiRssi=-43dBm&espIp=192.168.0.198&opType=7&content=startUp1132
@frappe.whitelist(allow_guest=True)
def upStat(*args, **kwargs):
    # print("\n------------Iot up status")
    add_new_ip_info(**kwargs)
    return "Iot up status ok"


# endpoint: http://127.0.0.1:8000/api/method/bbl_api.api01.iot_api.upData
@frappe.whitelist(allow_guest=True)
def upData(*args, **kwargs):
    # print("\n------------Iot upData")
    add_new_rcl_water_temp(**kwargs)
    return "Iot update ok"


def add_new_ip_info(**kwargs):
    doc = frappe.new_doc("IP Info")
    doc.update(
         {
            "ap_name": kwargs.get("wifiSsid"),
            "info_type": kwargs.get("opType"),
            "information": kwargs.get("content"),
            "iot_name": kwargs.get("espId"),
            "ip_address": kwargs.get("espIp"),
            "mac_address": kwargs.get("mac"),
            # "name": "espGas-01",
            "online": 1,
            # "state": kwargs.get(state),
            "wifi_rssi": kwargs.get("wifiRssi")
        }
    )
    doc.insert(ignore_permissions=True)
    frappe.db.commit()
    # print(f"new doc2:{doc}")


def add_new_rcl_water_temp(**kwargs):
    doc = frappe.new_doc("Rcl Water Temp")
    doc.update(
         {
			"esp_name": kwargs.get("deviceId"),
			"dev_name": kwargs.get("deviceName"),
			"dev_type":kwargs.get("deviceType"),
			"temperature": kwargs.get("tempFloat"),
			"query_count": kwargs.get("queryCnt"),
			"query_failed": kwargs.get("queryFailed"),
			"update_count": kwargs.get("updateCnt"),
			"update_failed": kwargs.get("updateFailed"),
            "start_long": kwargs.get("timestamp")
		 }
    )
    doc.insert(ignore_permissions=True)
    frappe.db.commit()
    # print(f"new water doc:{doc}")

""" 调试测试用，还没有用 """
def test(**kwargs):
    t1 = kwargs.get("timestamp")
    doc = frappe.new_doc("Rcl Water Temp")
    print("wtt test()")
    print(t1)
    print(doc)

class IotError(Exception):
	http_status_code = 419



""" addUser 示例 """
""" 

def add_user_for_sites(
	context, email, first_name, last_name, user_type, send_welcome_email, password, add_role
):
	"Add user to a site"
	import frappe.utils.user

	for site in context.sites:
		frappe.connect(site=site)
		try:
			add_new_user(email, first_name, last_name, user_type, send_welcome_email, password, add_role)
			frappe.db.commit()
		finally:
			frappe.destroy()
	if not context.sites:
		raise IotError

def add_new_user(
	email,
	first_name=None,
	last_name=None,
	user_type="System User",
	send_welcome_email=False,
	password=None,
	role=None,
):
	user = frappe.new_doc("User")
	user.update(
		{
			"name": email,
			"email": email,
			"enabled": 1,
			"first_name": first_name or email,
			"last_name": last_name,
			"user_type": user_type,
			"send_welcome_email": 1 if send_welcome_email else 0,
		}
	)
	user.insert()
	user.add_roles(*role)
	if password:
		from frappe.utils.password import update_password

		update_password(user=user.name, pwd=password) """

