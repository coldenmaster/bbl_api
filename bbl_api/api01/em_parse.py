import frappe
from frappe.utils.data import add_to_date, now_datetime

from bbl_api.utils import WT_DATETIME_FORMAT, print_blue, print_blue_pp, print_green_pp, print_red, send_wechat_msg_admin_site, send_wechat_msg_em_app
# from bbl_api.utils import *



def parse_em_mqtt_str(**kwargs):
    # print_blue_pp(kwargs)
    # json_obj = json.loads(kwargs["payload"])
    # print_blue_pp(json_obj)
    msgs = kwargs.get("msg", "").split(",")
    # print_blue_pp(msgs)
    em_obj = {}
    for msg in msgs:
        msg = msg.strip()
        # print("msg:", len(msg),msg)
        if not msg_ok(msg):
            continue
        if 'em_id' not in em_obj:   
            em_obj['em_id'] = parse_em_id(msg)
        if (em_obj['em_id'] != parse_em_id(msg)):
            print("em_id wrong", parse_em_id(msg))
            continue
        
        # em_obj['data_len'] = data_len(msg)
        # em_obj[data_cmd(msg)] = data_data(msg, data_len(msg))
        dataProc(data_cmd(msg), data_data(msg, data_len(msg)), em_obj)
        
    # print_blue(em_obj)
    return em_obj
    
def parse_em_id(msg):
    return reverse_hex_string(msg[2:14])

def data_len(msg):
    return int(msg[2*9:2*9+2], 16) # 有效数据的长度

def data_cmd_flag(msg):
    return msg[2*8:2*8+2] # always == '91'

def data_cmd(msg):
    # return reverse_hex_string(msg[2*10:2*14])
    return bcdStrProc33(reverse_hex_string(msg[2*10:2*14]), False)
def data_data(msg, len):
    return bcdStrProc33(reverse_hex_string(msg[2*14:2*14+len*2]), False)
    

def reverse_hex_string(str):
    if len(str) % 2 != 0:
        str = "0" + str
    sb = ""
    for i in range(len(str) - 2, -1, -2):
        sb += str[i]
        sb += str[i + 1]
    return sb

def bcdPlus33(s2):
    s2 = s2.upper()
    b1 = hex(int(s2, 16) + 51)[2:].upper()
    if s2 == "FF":
        b1 = b1[1:]
    return b1

def bcdSub33(s2):
    s2 = s2.upper()
    b1 = hex((int(s2, 16) - 51) & 0xFF)[2:].upper()
    if s2 == "32":
        b1 = "FF"
    elif len(b1) == 1:
        b1 = "0" + b1
    return b1

def bcdStrProc33(data_hex, plus_or_sub):
    sb = ''
    for i in range(0, len(data_hex), 2):
        if plus_or_sub:
            sb += bcdPlus33(data_hex[i:i + 2])
        else:
            sb += bcdSub33(data_hex[i:i + 2])
    return sb

def get_dtid(cmd):
    return cmd[0:2],cmd[2:4],cmd[4:6],cmd[6],

def parse_one_data(data_str, fmt, mom_dict, data_name):
    if len(data_str) < 8 and data_str[0] == "8":
        data_str = "-" + data_str[1:]
    data_num = float(data_str) * fmt
    mom_dict[data_name] = data_num


def parse_all_date(data_str, perLong, fmt, mom_dict, names):
    # print(data_str, perLong, fmt, mom_dict, names)
    if len(data_str) % perLong != 0:
        return
    cnt = len(data_str) // perLong
    # print_red(cnt)
    for i in range(cnt):
        parse_one_data(data_str[i * perLong:(i + 1) * perLong], fmt, mom_dict, names[i])

def dataProc(cmd, data_str, mom_dict):
    dtid0, dtid1, dtid2, dtid3  = get_dtid(cmd)
    # print("dtid:", dtid0, dtid1, dtid2, dtid3 )
    if dtid0 == "00": # 用电量
        if dtid1 == "00":
            names = ("et1", "et2", "et3", "et4", "et")
            parse_all_date(data_str, 8, 0.01, mom_dict, names)
        else:
            pass # 单独接收，还未处理
    elif dtid0 == "02":  # 电参数    
        if dtid1 == "01": # 电压
            if dtid2 == "FF": #全部
                names = ("ua", "ub", "uc")
                parse_all_date(data_str, 4, 0.1, mom_dict, names)
        elif dtid1 == "02": # 电流
            if dtid2 == "FF": #全部
                names = ("ia", "ib", "ic")
                parse_all_date(data_str, 6, 0.001, mom_dict, names)
        elif dtid1 == "03": # 功率
            if dtid2 == "FF": #全部
                names = ("pt", "pa", "pb", "pc")
                parse_all_date(data_str, 6, 0.0001, mom_dict, names)
        elif dtid1 == "06": # 功率因数
            if dtid2 == "FF": #全部
                names = ("pfa", "pfb", "pfc", "pf")
                parse_all_date(data_str, 4, 0.001, mom_dict, names)

def msg_ok(msg):
    if len(msg) < 24:
        return False
    if msg[0] != "6" \
    or msg[1] != "8" \
    or msg[14] != "6" \
    or msg[15] != "8" :
        return False
    return True

def correct_em_data(em_obj, tv, tc):
    try:
        pw = tv * tc
        em_obj.et = em_obj.get("et", 0) * pw / 1000
        em_obj.et1 = em_obj.get("et1", 0) * pw / 1000
        em_obj.et2 = em_obj.get("et2", 0) * pw / 1000
        em_obj.et3 = em_obj.get("et3", 0) * pw / 1000
        em_obj.et4 = em_obj.get("et4", 0) * pw / 1000
        em_obj.pt = em_obj.get("pt", 0) * pw 
        em_obj.pa = em_obj.get("pa", 0) * pw
        em_obj.pc = em_obj.get("pc", 0) * pw
        em_obj.ua = em_obj.get("ua", 0) * tv
        em_obj.uc = em_obj.get("uc", 0) * tv
        em_obj.ia = em_obj.get("ia", 0) * tc
        em_obj.ic = em_obj.get("ic", 0) * tc
        return True
    except Exception as e:
        print_red(f"Error in correct_em_data: {em_obj}")
        # frappe.traceback()
        return False
    
    
 # report period
def em_perday(delta:int = 0):
    # 计算时间区间，可以使用此程序运行时间，或者使用固定时间
    report_type = '日报'
    now_time = now_datetime()
    now_time = add_to_date(now_time, days=delta)
    end_time = now_time.replace(hour=0, minute=0, second=0, microsecond=0)
    start_time = add_to_date(end_time, days=-1)
    msg = f"电表日报\nstart_time:{start_time}\n end_time: {end_time}"
    # print_blue(msg)
    # send_wechat_msg_admin_site(msg)
    
    # 获取电表列表
    doc = 'Elec Meter RT'
    li = em_list(doc, start_time, end_time)
    
    wx_msg = f'<< 用电量报告-{report_type} >>\n'
    for em_name in li:
        wx_msg += em_calc(doc, report_type, em_name, start_time, end_time)
    # print_green_pp(wx_msg)
    send_wechat_msg_em_app(wx_msg)

def em_permonth(delta:int = 0):
    report_type = '月报'
    now_time = now_datetime()
    now_time = add_to_date(now_time, months=delta)
    end_time = now_time.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    start_time = add_to_date(end_time, months=-1)
    msg = f"电表月报\nstart_time:{start_time}\n end_time: {end_time}"
    send_wechat_msg_admin_site(msg)
    doc = 'Elec Meter Report'
    li = em_list(doc, start_time, end_time)
    
    wx_msg = f'<< 用电量报告-{report_type} >>\n'
    for em_name in li:
        wx_msg += em_calc_mon(report_type, em_name, start_time, end_time)
    # print_green_pp(wx_msg)
    send_wechat_msg_em_app(wx_msg)

def em_list(doc, start_time, end_time):
    li = frappe.db.get_list(doc, 
                    filters =  {
                        'for_date': ('between', [start_time, end_time]),
                    },
                    pluck = 'em_name',
                    distinct = True,
                    ignore_ifnull = True)
    # print_blue_pp(li)
    return li

def em_calc(doc, report_type, em_name, start_time, end_time):
    li = frappe.db.get_list(doc, 
                            filters =  {
                                'em_name': em_name,
                                'for_date': ('between', [start_time, end_time]),
                            },
                            # fields=['em_name', 'modified' ,'et', 'name'],
                            fields=['*'],
                            order_by='for_date asc',
                            )
    return em_mk_report(em_name, report_type, li)
    
    
def em_calc_mon(report_type, em_name, start_time, end_time):
    li = frappe.db.get_list('Elec Meter Report', 
                            filters =  {
                                'em_name': em_name,
                                'report_period': '日报',
                                'for_date': ('between', [start_time, end_time]),
                            },
                            # fields=['em_name', 'modified' ,'et', 'name'],
                            fields=['*'],
                            order_by='for_date asc',
                            )
    return em_mk_report(em_name, report_type, li)
    
def em_mk_report(em_name, report_type, li):
    # print_blue_pp(li)
    # print_red(f'{em_name} list cnt: {len(li)}')
    if not li:
        return
    doc_first = li[0]
    doc_last = li[-1]
    em_et_sub(doc_last, doc_first)
    doc_last.pt = max(em.pt for em in li)
    doc_last.pa = max(em.pa for em in li)
    doc_last.pc = max(em.pc for em in li)
    doc_last.pf = min(em.pf for em in li)
    doc_last.doctype = 'Elec Meter Report'
    doc_last.report_period = report_type
    # doc_last.for_date = doc_last.modified
    
    wx_msg = f'------\n设备名称: {em_name}\n'
    wx_msg += f'开始时间: {doc_first.for_date.strftime(WT_DATETIME_FORMAT)}\n'
    wx_msg += f'结束时间: {doc_last.for_date.strftime(WT_DATETIME_FORMAT)}\n'
    wx_msg += f'电表读数: {doc_last.et}\n'
    wx_msg += f' 用电量 : {doc_last.et_sub:>.3f} 千度\n'
    wx_msg += f'最大功率: {doc_last.pt} Kw\n'
    
    new_em_report = frappe.get_doc(doc_last)
    new_em_report.insert(ignore_permissions=True)
    frappe.db.commit()
    return wx_msg

def em_et_sub(last, first):
    last.et_sub = last.et - first.et
    last.et1_sub = last.et1 - first.et1
    last.et2_sub = last.et2 - first.et2
    last.et3_sub = last.et3 - first.et3
    last.et4_sub = last.et4 - first.et4
    


# if __name__ == "__main__":

# up_kwargs = {
#     "username": "undefined", 
#     "topic": "esp/s/d", 
#     "timestamp": 1709632574840, 
#     "qos": 0, 
#     "publish_received_at": 1709632574840, 
#     "pub_props": {"User-Property": {}}, 
#     "peerhost": "117.153.11.255", 
#     "payload": '''{
#         "espId":"espEmGy",
#         "deviceType":"EM",
#         "mac":"30:83:98:92:10:FA",
#         "wifiSsid":"HIKbs",
#         "wifiRssi":"-34dBm",
#         "espIp":"192.168.0.194",
#         "opType":"EM_DATA",
#         "timestamp":3323,
#         "msg":",687098580000906891183332333367443333333333334c333333a5353333753b3333,\
#             6870985800009068911033323635333333333333333333333333,\
#             6870985800009068910a33323435333333333333,\
#             6870985800009068910d33323535333333333333333333,\
#             6870985800009068910c333239353343334333333343"
#         }''',
#     "node": "emqx@172.18.0.7",
#     "metadata": {"rule_id": "dev_esp_frappe_WH_D"},
#     "id": "000612E6DA51DDA3618C22002CA5014B", 
#     "event": "message.publish", 
#     "clientid": "espEmGy-69", 
#     "cmd": "bbl_api.api01.iot_api.esp"
# }

# class ElecMeter:
#     pass

#     parse_em_mqtt_str(**up_kwargs)

