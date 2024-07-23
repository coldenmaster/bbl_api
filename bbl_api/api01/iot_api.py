import json
import frappe
from frappe.utils import today, add_to_date
from frappe.utils.data import get_timestamp, now, now_datetime

# from wechat_work.utils import send_str_to_admin
from bbl_api.api01.em_parse import em_perday, em_permonth
from bbl_api.api01.iot_service import *
from bbl_api.api01.zpl import zpl_perday
from bbl_api.utils import *

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
    # print_cyan( f"from mqtt esp/out rev:, { str(kwargs) }")
    # print_green_pp(kwargs)
    obj = frappe._dict(kwargs)
    # espWho = obj.clientid.split('-')[0] or "espNew"
    timeUtc = obj.publish_received_at or get_timestamp(now_datetime())
    try:
        jsonPayload = json.loads(obj.payload)
    except:
        jsonPayload = {
            "content": obj.payload,  # payload是单字符串的处理
        }
    jsonPayload['espWho'] = jsonPayload.get('espId') or "espNew"
    jsonPayload['timeUtc'] = timeUtc / 1000
    # jsonPayload['msgType'] = obj.topic
    # jsonPayload['opType'] = 'esp_rcl_water_temp'
    # print_green_pp(jsonPayload)

    devDoc = get_dev_doc(jsonPayload.get('espWho'))
    # jsonPayload['dev_type_db'] = devDoc.device_type
    # jsonPayload['dev_name_db'] = devDoc.device_name
    jsonPayload['dev_doc'] = devDoc

    add_new_ip_info(**jsonPayload)

    if '中频炉测温' == devDoc.device_type:
        add_esp_adc_base(**jsonPayload)
    elif jsonPayload.get('opType', '') == 'WATER_TEMP':
        add_new_rcl_water_temp(**jsonPayload)
    # todo 改为 espId 中
    elif jsonPayload.get('deviceType', '') == 'EM':  # 注意这个判断放在前面，会拦截了别的处理
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

    
    
# http://127.0.0.1:8000/api/method/bbl_api.api01.iot_api.pad_em_day?delta=-1
@frappe.whitelist(allow_guest=True)
def pad_em_day(*args, **kwargs):
    """
    通过 API 部缺失的电表日报
    """
    delta = int(kwargs.get("delta", 0))
    em_perday(delta)
    rt = f"补填电表日报：{delta} 天"
    return rt

# http://127.0.0.1:8000/api/method/bbl_api.api01.iot_api.pad_em_mon?delta=-1
@frappe.whitelist(allow_guest=True)
def pad_em_mon(*args, **kwargs):
    delta = int(kwargs.get("delta", 0))
    em_permonth(delta)
    rt = f"补填电表月报：{delta} 月"
    return rt

# http://127.0.0.1:8000/api/method/bbl_api.api01.iot_api.pad_zpl_day?delta=-1
@frappe.whitelist(allow_guest=True)
def pad_zpl_day(*args, **kwargs):
    delta = int(kwargs.get("delta", 0))
    zpl_perday(delta)
    rt = f"补填中频炉日数据：{delta} 日"
    return rt


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
    # print_green(rt)
    return rt

    
# todo 服务器上准备删除(在frappe系统内日志设定中自动删除)
# http://erp15.hbbbl.top:82/api/method/bbl_api.api01.iot_api.delTemp
# http://127.0.0.1:8000/api/method/bbl_api.api01.iot_api.delTemp?days=-20
@frappe.whitelist(allow_guest=True)
def delTemp(*args, **kwargs):
    last_date = add_to_date(today(), days=int(kwargs.get('days', -30)))
    # print(last_date)
    frappe.db.delete('Rcl Water Temp', {
        "modified": ("<=", last_date)}
        )
    frappe.db.commit()
    msg = f"delete Rcl Water Temp <= { last_date } days, ok"
    # send_str_to_admin(msg)
    bbl_mqtt_client.publish('testtopic/2', msg)
    return msg


# todo 服务器上准备删除(在frappe系统内日志设定中自动删除)
# http://erp15.hbbbl.top:82/api/method/bbl_api.api01.iot_api.delIpInfo
# http://127.0.0.1:8000/api/method/bbl_api.api01.iot_api.delIpInfo?days=-20
@frappe.whitelist(allow_guest=True)
def delIpInfo(*args, **kwargs):
    last_date = add_to_date(today(), days=int(kwargs.get('days', -30)))
    # print(last_date)
    frappe.db.delete('IP Info', {
        "modified": ("<=", last_date)}
        )
    frappe.db.commit()
    msg = f"delete IP Info Records <= { last_date } days, ok"
    # send_str_to_admin(msg)
    return msg


# 接收esp直径连接的api，接收各种状态汇报
# endpoint: 
# http://127.0.0.1:8000/api/method/bbl_api.api01.iot_api.upStat
# http://127.0.0.1:8000/api/method/bbl_api.api01.iot_api.upStat?espId=espGas&wifiSsid=HIKbs3&mac=F4:CF:A2:F7:5D:4C&wifiRssi=-43dBm&espIp=192.168.0.198&opType=7&content=startUp1132
# http://erp15.hbbbl.top:82/api/method/bbl_api.api01.iot_api.upStat
# http://erp15.hbbbl.top:82/api/method/bbl_api.api01.iot_api.upStat?espId=espGas&wifiSsid=HIKbs3&mac=F4:CF:A2:F7:5D:4C&wifiRssi=-43dBm&espIp=192.168.0.198&opType=7&content=startUp1132
@frappe.whitelist(allow_guest=True)
def upStat(*args, **kwargs):
    # print_cyan( f"esp http upStat 上传状态:, { str(kwargs) }")
    espId = kwargs.get('espId', 'no espId')
    upType = kwargs.get('opType', 'no opType')
    up_msg = kwargs.get('content', 'no msg')
    # print_blue( f"esp http upStat 上传状态: id:{ espId }, type:{ upType }, content:{ up_msg }")
    if upType == 'GET_LOST':
        # frappe.local.response.http_status_code = 416
        return 'get_lost_ok'
    if upType == 'HEART_BEAT':
        return 'heart_beat_ok'
   
    return 'upStat OK'


# 接收esp直径连接的api，接收各种数据使用（现在还没有esp使用此接口）
# endpoint: 
# http://127.0.0.1:8000/api/method/bbl_api.api01.iot_api.upData?deviceId=espGas&deviceName=a32&deviceType=a3&tempFloat=33&queryCnt=44&queryFailed=55&updateCnt=66&updateFailed=77
@frappe.whitelist(allow_guest=True)
def upData(*args, **kwargs):
    print_cyan( f"esp http upData 上传app数据: { str(kwargs) }")
    
     # user = frappe.session.user
    # logger.info(f"{user} access upDate" )  # Guess
    # obj = frappe._dict(kwargs)
    kwargs['espWho'] = kwargs.get('deviceId', 'espNew')
    # print_blue(f'kw: {str(kwargs)}')
    # print_blue(f'obj: {str(obj)}')
    # add_new_rcl_water_temp(**kwargs)
    return "Iot update ok"


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

