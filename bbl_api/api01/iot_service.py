
from frappe.utils import today, add_to_date
from frappe.utils.data import cint, get_timestamp, now, now_datetime

from bbl_api.api01.em_parse import correct_em_data, parse_em_mqtt_str
from bbl_api.utils import *


def parse_em_data(**kwargs):
    if kwargs.get('opType', '') != 'EM_DATA':
        return
    em_dict = parse_em_mqtt_str(**kwargs)
    em_obj = frappe._dict(em_dict)
    # print_green(em_obj)
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
    tv = cint(dev_doc.value_one) if cint(dev_doc.value_one) else 1
    tc = cint(dev_doc.value_two) if cint(dev_doc.value_two) else 1
    # print("tv, tc", tv, tc)
    correct_em_data(em_obj, tv, tc)

    
    # 新建电表记录
    em_obj.doctype = 'Elec Meter RT'
    em_obj.em_address = em_addr
    em_obj.em_name = dev_doc.device_name
    em_obj.em_type = dev_doc.device_type
    em_obj.for_date = now()
    new_em_doc = frappe.get_doc(em_obj)
    # print_blue_pp(new_em_doc)
    # print_blue(em_obj)
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
            # print_red('保存esp上传的温度报警')
    
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
    
    
def add_esp_adc_base(**kwargs):
    obj = frappe._dict(kwargs)
    # print_red(f"进入中频炉测温处理 {obj.get('espWho')=}")
    # print_green_pp(obj)
    # 查询设备信息，对比报警信息
    dev_doc = obj.dev_doc
    deviceName = dev_doc.device_name or "espNew"
    deviceType = dev_doc.device_type or "espType"
    print_yellow(f'deviceName:{deviceName}')
    
    newDoc = frappe.get_doc(
        {
            "doctype": "Esp Adc Base",
            # "esp_name": obj.deviceId,
            "esp_name": obj.dev_doc.name,
            "dev_name": deviceName,
            "dev_type": deviceType,
            "op_type": obj.opType,
            "poweron_duration": obj.timestamp,
            "query_count": obj.queryCnt,
            "update_count": obj.updateCnt,
            "adc_value": obj.adcValue,
            "target_value": obj.targetValue,
            "display_value": obj.targetValue_f,
            "target_top": obj.tempTop,
            "target_bottom": obj.tempIdx,
            "target_count": obj.tempCnt,
            "product_quantity": obj.quantity,
            "out_interval": obj.outIntv,
        }
    )
    newDoc.insert(ignore_permissions=True)
    frappe.db.commit()
    
def get_dev_doc(dev_name):
    dev_doc = {}
    try:
        dev_doc = frappe.get_doc("Iot Device", dev_name)
    except:
        print_red(f"没有{dev_name}，新建一条设备信息")
        dev_doc = frappe.new_doc("Iot Device")
        dev_doc.iot_name = dev_name
        dev_doc.device_name = '未知设备'
        dev_doc.save(ignore_permissions=True)
        frappe.db.commit()
    return dev_doc

def add_new_ip_info(**kwargs):
    # print_blue(f"add_new_ip_info: kwargs:{ kwargs }")
    obj = frappe._dict(kwargs)
    devDoc = obj.dev_doc
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
            "information": obj.content or obj.opType,
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
    if (obj.opType == 'POWER_ON'):
        key = f"iot_id:{obj.dev_name}:{obj.opType}"
        if not frappe.cache.get_value(key):
            frappe.cache.set_value(key, True, expires_in_sec=60*30)
            msg = f'{newDoc.dev_name} 开机\n'
            msg += f'{newDoc.ip_address}@{newDoc.ap_name}'
            # send_wechat_msg_admin_site(msg)


def compare_alarm_info(upHigh, upLow, savHigh, savLow):
    msg = f"报警温度设定不成功: upHigh:{upHigh} savHigh:{savHigh} | upLow:{upLow} savLow:{savLow}"
    if upHigh != savHigh or upLow != savLow:
        # send_str_to_admin(msg)
        # frappe.log_error("温度设定不成功", msg)
        # logger.error(msg)
        # print_yellow(msg)
        return True
    return False
    