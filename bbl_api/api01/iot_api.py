import json
import frappe
from frappe.utils import today, add_to_date

from wechat_work.utils import send_str_to_admin
from bbl_api.utils import *

# from mqtt.mqtt_rt import mqtt_route, bbl_mqtt_client
from mqtt.mqtt_rt import bbl_mqtt_client

# frappe.utils.logger.set_log_level('DEBUG')
logger = frappe.logger("iot")

_mqtt_esp_url = 'http://127.0.0.1:8000/api/method/bbl_api.api01.iot_api.esp'

# def mqtt_register():
#     mqtt_route.register_topic_rt("esp/#", _mqtt_esp_url)

@frappe.whitelist(allow_guest=True)
def publish(msg, topic = 'esp/in'):
    bbl_mqtt_client.publish(topic, msg)


# 已经取消了on_message向这里转发，使用mqtt服务器向这里进行转发
# mqtt 接收数据api 
# http://127.0.0.1:8000/api/method/bbl_api.api01.iot_api.esp
@frappe.whitelist(allow_guest=True)
def esp(*args, **kwargs):
    # print_cyan( f"from mqtt esp/out rev:, { str(kwargs) }")
    # pprint(kwargs)
    obj = frappe._dict(kwargs)
    espWho = obj.clientid.split('-')[0] or "espNew"
    timeUtc = obj.publish_received_at
    jsonPayload = json.loads(obj.payload)
    jsonPayload['espWho'] = espWho
    jsonPayload['timeUtc'] = timeUtc / 1000
    # jsonPayload['msgType'] = obj.topic
    jsonPayload['msgType'] = 'esp_rcl_water_temp'
    # print(jsonPayload)
    
    add_new_ip_info(**jsonPayload)
    
    match jsonPayload['msgType']:
        case 'esp_rcl_water_temp':
            add_new_rcl_water_temp(**jsonPayload)
        case _:
            print_red("no match mqtt route.")
    # send_str_to_admin(rt)
    frappe.db.commit()
    return "mqtt rev ok"


def add_new_rcl_water_temp(**kwargs):
    obj = frappe._dict(kwargs)
    # print_red(f'obj:{obj}')
    devDoc = {}
    # 查询设备信息，对比报警信息
    try:
        devDoc = frappe.get_doc("Iot Device", obj.espWho)
    except:
        devDoc = frappe.new_doc("Iot Device")
    
    # deviceId = obj.espWho or "espNew"
    # deviceName = frappe.db.get_value("Iot Device", deviceId, "device_name")
    deviceName = devDoc.device_name or "espNew"
    # print_yellow(f'deviceName:{deviceName}')
    
    if deviceName != "espNew":
        compare_alarm_info(obj.tempHigh, obj.tempLow, devDoc.alarm_val_one, devDoc.alarm_val_two)
    
    newDoc = frappe.get_doc(
        {
            "doctype": "Rcl Water Temp",
            "esp_name": obj.deviceId,
            "dev_name": deviceName,
            # "dev_type": obj.deviceType,
            "temperature": obj.tempFloat,
            "query_count": obj.queryCnt,
            "query_failed": obj.queryFailed,
            "update_count": obj.updateCnt,
            "update_failed": obj.updateFailed,
            "start_long": obj.timestamp,
            # 插入数据库时会被更改
            # "creation": time.strftime("%Y-%m-%d %H:%M:%S", timeArray),
            # "modified": time.strftime("%Y-%m-%d %H:%M:%S", timeArray),
        }
    )
    newDoc.insert(ignore_permissions=True)
    # frappe.db.commit()
    # print_cyan(f"new doc:{vars(newDoc)}")

def add_new_ip_info(**kwargs):
    # logger.error(f"add_new_ip_info: kwargs:{ kwargs}")
    obj = frappe._dict(kwargs)
    devDoc = {}
    try:
        devDoc = frappe.get_doc("Iot Device", obj.espWho)
    except:
        devDoc = frappe.new_doc("Iot Device")
    ip_info = obj.espIp + "@" + obj.wifiSsid
    if (devDoc.ip_info != ip_info):
        devDoc.db_set('ip_info', ip_info)
    if (devDoc.value_one != obj.tempFloat):
        devDoc.db_set('value_one', obj.tempFloat,  update_modified=False)
    # devDoc.save(ignore_permissions=True)
    newDoc = frappe.get_doc(
         {
            "doctype": "IP Info",
            "ap_name": obj.wifiSsid,
            "info_type": obj.opType,
            "information": obj.content,
            "iot_name": obj.espWho,
            "dev_name": obj.espId,
            "cn_name": devDoc.device_name or "espNew",
            "ip_address": obj.espIp,
            "mac_address": obj.mac,
            "online": 1,
            # "state": kwargs.get(state),
            "wifi_rssi": obj.wifiRssi
        }
    )
    newDoc.insert(ignore_permissions=True)
    # frappe.db.commit()
    return "Iot up status ok"
    

def compare_alarm_info(upHigh, upLow, savHigh, savLow):
    msg = f"报警温度设定不成功: upHigh:{upHigh} savHigh:{savHigh} | upLow:{upLow} savLow:{savLow}"
    if upHigh != savHigh or upLow != savLow:
        # send_str_to_admin(msg)
        # frappe.log_error("温度设定不成功", msg)
        # logger.error(msg)
        print_yellow(msg)

# mqtt 发送数据api
# http://127.0.0.1:8000/api/method/bbl_api.api01.iot_api.pub01?msg=abc123def&topic=esp/in
# http://127.0.0.1:8000/api/method/bbl_api.api01.iot_api.pub01?msg={"msg":"hello","deviceId":"espTzxWater3","tempHigh":49,"tempLow":18}
@frappe.whitelist(allow_guest=True)
def pub01(*args, **kwargs):
    """
    通过 API 发送 mqtt 到 指定 topic
    """
    msg = kwargs.get("msg", "shan上下五千年ok123abc")
    topic = kwargs.get("topic", "esp/in")
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
    msg = f"delete Rcl Water Temp <= { last_date } days, ok"
    send_str_to_admin(msg)
    bbl_mqtt_client.publish('testtopic/2', msg)
    return msg


# http://erp15.hbbbl.top:82/api/method/bbl_api.api01.iot_api.delIpInfo
# http://127.0.0.1:8000/api/method/bbl_api.api01.iot_api.delIpInfo?days=-20
@frappe.whitelist(allow_guest=True)
def delIpInfo(*args, **kwargs):
    last_date = add_to_date(today(), days=int(kwargs.get('days', -30)))
    print(last_date)
    frappe.db.delete('IP Info', {
        "modified": ("<=", last_date)}
        )
    frappe.db.commit()
    msg = f"delete IP Info Records <= { last_date } days, ok"
    send_str_to_admin(msg)
    return msg


# endpoint: 
# http://127.0.0.1:8000/api/method/bbl_api.api01.iot_api.upStat
# http://127.0.0.1:8000/api/method/bbl_api.api01.iot_api.upStat?espId=espGas&wifiSsid=HIKbs3&mac=F4:CF:A2:F7:5D:4C&wifiRssi=-43dBm&espIp=192.168.0.198&opType=7&content=startUp1132
# http://erp15.hbbbl.top:82/api/method/bbl_api.api01.iot_api.upStat
# http://erp15.hbbbl.top:82/api/method/bbl_api.api01.iot_api.upStat?espId=espGas&wifiSsid=HIKbs3&mac=F4:CF:A2:F7:5D:4C&wifiRssi=-43dBm&espIp=192.168.0.198&opType=7&content=startUp1132
@frappe.whitelist(allow_guest=True)
def upStat(*args, **kwargs):
    # print("\n------------Iot up status")
    return add_new_ip_info(**kwargs)


# todo 服务器上准备删除
# endpoint: 
# http://127.0.0.1:8000/api/method/bbl_api.api01.iot_api.upData?deviceId=espGas&deviceName=a32&deviceType=a3&tempFloat=33&queryCnt=44&queryFailed=55&updateCnt=66&updateFailed=77
@frappe.whitelist(allow_guest=True)
def upData(*args, **kwargs):
    # user = frappe.session.user
    # logger.info(f"{user} access upDate" )  # Guess
    add_new_rcl_water_temp(**kwargs)
    return "Iot update ok"


# def add_new_ip_info(**kwargs):
#     logger.error(f"add_new_ip_info: kwargs:{ kwargs}")
#     try:
#         if (not kwargs.get("espId")):
#             return "add_new_ip_info: no espId"
#         devDoc = frappe.get_doc("Iot Device", kwargs.get("espId", "espNew"))
#     except:
#         devDoc = frappe.new_doc("Iot Device")
#     doc = frappe.new_doc("IP Info")
#     # 获取此信息设备的相关信息
#     # print(f"new devDoc:{devDoc}")
#     doc.update(
#          {
#             "ap_name": kwargs.get("wifiSsid"),
#             "info_type": kwargs.get("opType"),
#             "information": kwargs.get("content"),
#             "iot_name": kwargs.get("espId"),
#             "cn_name": devDoc.device_name,
#             "ip_address": kwargs.get("espIp"),
#             "mac_address": kwargs.get("mac"),
#             # "name": "espGas-01",
#             "online": 1,
#             # "state": kwargs.get(state),
#             "wifi_rssi": kwargs.get("wifiRssi")
#         }
#     )
#     doc.insert(ignore_permissions=True)
#     frappe.db.commit()
#     return "Iot up status ok"
    


# def add_new_rcl_water_temp(**kwargs):
#     # devDoc = frappe.get_doc("Iot Device", {"iot_name": kwargs.get("deviceId")})
#     devDoc = frappe.get_doc("Iot Device", kwargs.get("deviceId", "espNew"))

#     # print(f"new devDoc:{devDoc}")
#     doc = frappe.new_doc("Rcl Water Temp")
#     doc.update(
#          {
# 			"esp_name": kwargs.get("deviceId"),
# 			# "dev_name": devDoc.get("deviceName"),
# 			"dev_name": devDoc.device_name,
# 			"dev_type":kwargs.get("deviceType"),
# 			"temperature": kwargs.get("tempFloat"),
# 			"query_count": kwargs.get("queryCnt"),
# 			"query_failed": kwargs.get("queryFailed"),
# 			"update_count": kwargs.get("updateCnt"),
# 			"update_failed": kwargs.get("updateFailed"),
#             "start_long": kwargs.get("timestamp")
# 		 }
#     )
#     doc.insert(ignore_permissions=True)
#     frappe.db.commit()

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

