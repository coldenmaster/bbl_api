import json
import frappe
from frappe.utils import today, add_to_date
from frappe.utils.data import now

from wechat_work.utils import send_str_to_admin
from bbl_api.api01.em_parse import correct_em_data, parse_em_mqtt_str
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



""" 
    esp8266通过mqtt发送上来的数据，都转发到这里，进行分类处理：
    1.通过deviceType（上传的）进行分类
    2.新设备找不到总数包ex，需要提前处理。

"""


# 已经取消了on_message向这里转发，使用mqtt服务器向这里进行转发
# mqtt 接收数据api 
# http://127.0.0.1:8000/api/method/bbl_api.api01.iot_api.esp
@frappe.whitelist(allow_guest=True)
def esp(*args, **kwargs):
    print_cyan( f"from mqtt esp/out rev:, { str(kwargs) }")
    # print_green_pp(kwargs)
    obj = frappe._dict(kwargs)
    # espWho = obj.clientid.split('-')[0] or "espNew"
    timeUtc = obj.publish_received_at
    try:
        jsonPayload = json.loads(obj.payload)
    except:
        jsonPayload = {
            "content": obj.payload,  # payload是单字符串的处理
        }
    jsonPayload['espWho'] = jsonPayload.get('espId')
    jsonPayload['timeUtc'] = timeUtc / 1000
    # jsonPayload['msgType'] = obj.topic
    # jsonPayload['opType'] = 'esp_rcl_water_temp'
    # print_green_pp(jsonPayload)
    
    add_new_ip_info(**jsonPayload)
    
    if jsonPayload.get('opType', '') == 'WATER_TEMP':
        add_new_rcl_water_temp(**jsonPayload)
    if jsonPayload.get('deviceType', '') == 'EM':
        parse_em_data(**jsonPayload)
    # else:
    #     print_red("no match mqtt route.")
    
    # match jsonPayload['msgType']:
    #     case 'esp_rcl_water_temp':
    #         add_new_rcl_water_temp(**jsonPayload)
    #     case _:
    #         print_red("no match mqtt route.")
    # send_str_to_admin(rt)
    
    return "mqtt rev ok"

def parse_em_data(**kwargs):
    if kwargs.get('opType', '') != 'EM_DATA':
        return
    em_dict = parse_em_mqtt_str(**kwargs)
    em_obj = frappe._dict(em_dict)
    print_green(em_obj)
    # 找到是哪个电表，获取电表名称
    em_addr = em_obj.get('em_id', '9527')
    dev_doc = {}
    try:
        dev_doc = frappe.get_doc("Iot Device", em_addr)
    except:
        # 新建设备信息
        dev_doc = frappe.new_doc("Iot Device")
        dev_doc.iot_name = em_addr
        dev_doc.device_name = '未知电表'
        dev_doc.save(ignore_permissions=True)
        frappe.db.commit()
    
    # 取得电压比，电流比
    tv = int(dev_doc.value_one) if dev_doc.value_one.isdigit() else 1
    tc = int(dev_doc.value_two) if dev_doc.value_two.isdigit() else 1
    print("tv, tc", tv, tc)
    correct_em_data(em_obj, tv, tc)
    
    # 新建电表记录
    em_obj.doctype = 'Elec Meter RT'
    em_obj.em_address = em_addr
    em_obj.em_name = dev_doc.device_name
    em_obj.em_type = dev_doc.device_type
    em_obj.em_time = now()
    new_em_doc = frappe.get_doc(em_obj)
    # print_blue_pp(new_em_doc)
    new_em_doc.insert(ignore_permissions=True)
    frappe.db.commit()
    

    
    
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
        if compare_alarm_info(obj.tempHigh, obj.tempLow, devDoc.alarm_val_one, devDoc.alarm_val_two):
            """ 这里把esp卡上的设置温度保存到数据库，为了和esp上设置简单的同步
                todo 这样会造成服务器上设置不失效，应该改为esp卡上修改报警温度时发送mqtt信息
            """
            devDoc.db_set('alarm_val_one', obj.tempHigh)
            devDoc.db_set('alarm_val_two', obj.tempLow)
            print_red('保存esp上传的温度报警')
    
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
    frappe.db.commit()

def add_new_ip_info(**kwargs):
    # print_blue(f"add_new_ip_info: kwargs:{ kwargs }")
    obj = frappe._dict(kwargs)
    devDoc = {}
    try:
        devDoc = frappe.get_doc("Iot Device", obj.espWho)
    except:
        devDoc = frappe.new_doc("Iot Device")
        devDoc.save(ignore_permissions=True)
        frappe.db.commit()
    ip_info = "" + str(obj.espIp) + "@" + str(obj.wifiSsid)
    if (devDoc.ip_info != ip_info):
        devDoc.db_set('ip_info', ip_info)
    # todo 这里根据设备类型，过滤掉存储温度
    # todo 这里根据modified时间，处理10min内的存储ip记录
    if (devDoc.value_one != obj.tempFloat):
        devDoc.db_set('value_one', obj.tempFloat, update_modified=False)
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
    frappe.db.commit()
    

def compare_alarm_info(upHigh, upLow, savHigh, savLow):
    msg = f"报警温度设定不成功: upHigh:{upHigh} savHigh:{savHigh} | upLow:{upLow} savLow:{savLow}"
    if upHigh != savHigh or upLow != savLow:
        # send_str_to_admin(msg)
        # frappe.log_error("温度设定不成功", msg)
        # logger.error(msg)
        print_yellow(msg)
        return True
    return False

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

    
# todo 服务器上准备删除(在frappe系统内日志设定中自动删除)
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


# todo 服务器上准备删除(在frappe系统内日志设定中自动删除)
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


# todo 服务器上准备删除
# endpoint: 
# http://127.0.0.1:8000/api/method/bbl_api.api01.iot_api.upStat
# http://127.0.0.1:8000/api/method/bbl_api.api01.iot_api.upStat?espId=espGas&wifiSsid=HIKbs3&mac=F4:CF:A2:F7:5D:4C&wifiRssi=-43dBm&espIp=192.168.0.198&opType=7&content=startUp1132
# http://erp15.hbbbl.top:82/api/method/bbl_api.api01.iot_api.upStat
# http://erp15.hbbbl.top:82/api/method/bbl_api.api01.iot_api.upStat?espId=espGas&wifiSsid=HIKbs3&mac=F4:CF:A2:F7:5D:4C&wifiRssi=-43dBm&espIp=192.168.0.198&opType=7&content=startUp1132
# @frappe.whitelist(allow_guest=True)
# def upStat(*args, **kwargs):
#     print_blue("\n esp http 上传状态")
#     # obj = frappe._dict(kwargs)
#     kwargs['espWho'] = kwargs.get('espId', 'espNew')
    
#     print_blue(f'kw: {str(kwargs)}')
#     # print_blue(f'obj: {str(obj)}')
#     return add_new_ip_info(**kwargs)


# todo 服务器上准备删除
# endpoint: 
# http://127.0.0.1:8000/api/method/bbl_api.api01.iot_api.upData?deviceId=espGas&deviceName=a32&deviceType=a3&tempFloat=33&queryCnt=44&queryFailed=55&updateCnt=66&updateFailed=77
@frappe.whitelist(allow_guest=True)
def upData(*args, **kwargs):
    print_blue("\n esp http 上传app数据")
        # user = frappe.session.user
    # logger.info(f"{user} access upDate" )  # Guess
    # obj = frappe._dict(kwargs)
    kwargs['espWho'] = kwargs.get('deviceId', 'espNew')
    print_blue(f'kw: {str(kwargs)}')
    # print_blue(f'obj: {str(obj)}')
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

