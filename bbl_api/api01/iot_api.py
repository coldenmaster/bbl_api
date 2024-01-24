import json
import frappe
from frappe.utils import today, add_to_date
from frappe.utils.data import now
import requests

from wechat_work.utils import send_str_to_admin
from bbl_api.utils import *

from mqtt.mqtt_rt import mqtt_route, bbl_mqtt_client

_mqtt_esp_url = 'http://127.0.0.1:8000/api/method/bbl_api.api01.iot_api.esp'

def mqtt_register():
    mqtt_route.register_topic_rt("esp/#", _mqtt_esp_url)

def publish(msg, topic = 'esp'):
    bbl_mqtt_client.publish(topic, msg)
# mqtt_register()

# mqtt 接收数据api
# http://127.0.0.1:8000/api/method/bbl_api.api01.iot_api.esp
@frappe.whitelist(allow_guest=True)
def esp(*args, **kwargs):
    rt = f"mqtt esp 控制器, { str(kwargs) }"
    print_cyan(rt)
    obj = frappe._dict(kwargs)
    # print_red(obj.payload)
    # send_str_to_admin(rt)
    return "mqtt in esp rev ok"

# mqtt 发送数据api
# http://127.0.0.1:8000/api/method/bbl_api.api01.iot_api.pub01?msg=abc123def&topic=esp
@frappe.whitelist(allow_guest=True)
def pub01(*args, **kwargs):
    """
    通过 API 发送 mqtt 到 指定 topic

    :param topic: 
    :param from: 
    :param to: 
    :type msg: dict | None | str
    """
    msg = kwargs.get("msg", "shan上下五千年ok123abc")
    topic = kwargs.get("topic", "esp")
    publish(msg, topic)
    rt = f"发送完成：{topic}: {msg}"
    print_green(rt)
    return rt

    

# http://erp15.hbbbl.top:82/api/method/bbl_api.api01.iot_api.delTemp
# http://127.0.0.1:8000/api/method/bbl_api.api01.iot_api.delTemp?days=-20
@frappe.whitelist(allow_guest=True)
def delTemp(*args, **kwargs):
    last_date = add_to_date(today(), days=int(kwargs.get('days', -30)))
    print(last_date)
    frappe.db.delete('Rcl Water Temp', {
        "modified": ("<=", last_date)}
        )
    frappe.db.commit()
    msg = f"delete Rcl Water Temp <= { last_date } date, ok"
    send_str_to_admin(msg)
    bbl_mqtt_client.publish('testtopic/2', "help me")
    return msg


# endpoint: http://127.0.0.1:8000/api/method/bbl_api.api01.iot_api.upStat
# http://127.0.0.1:8000/api/method/bbl_api.api01.iot_api.upStat?espId=espGas2&wifiSsid=HIKbs3&mac=F4:CF:A2:F7:5D:4C&wifiRssi=-43dBm&espIp=192.168.0.198&opType=7&content=startUp1132
# http://erp15.hbbbl.top:82/api/method/bbl_api.api01.iot_api.upStat?espId=espGas2&wifiSsid=HIKbs3&mac=F4:CF:A2:F7:5D:4C&wifiRssi=-43dBm&espIp=192.168.0.198&opType=7&content=startUp1132
@frappe.whitelist(allow_guest=True)
def upStat(*args, **kwargs):
    # print("\n------------Iot up status")
    add_new_ip_info(**kwargs)
    return "Iot up status ok"


# endpoint: 
# http://127.0.0.1:8000/api/method/bbl_api.api01.iot_api.upData?deviceId=espGas&deviceName=a32&deviceType=a3&tempFloat=33&queryCnt=44&queryFailed=55&updateCnt=66&updateFailed=77
@frappe.whitelist(allow_guest=True)
def upData(*args, **kwargs):
    # print("\n------------Iot upData")
    add_new_rcl_water_temp(**kwargs)
    return "Iot update ok"


def add_new_ip_info(**kwargs):
    doc = frappe.new_doc("IP Info")
    # 获取此信息设备的相关信息
    devDoc = frappe.get_doc("Iot Device", kwargs.get("espId"))
    # print(f"new devDoc:{devDoc}")
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


def add_new_rcl_water_temp(**kwargs):
    devDoc = frappe.get_doc("Iot Device", {"iot_name": kwargs.get("deviceId")})
    # print(f"new devDoc:{devDoc}")
    doc = frappe.new_doc("Rcl Water Temp")
    doc.update(
         {
			"esp_name": kwargs.get("deviceId"),
			# "dev_name": devDoc.get("deviceName"),
			"dev_name": devDoc.get_title(),
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

