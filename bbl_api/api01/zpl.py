import frappe
import datetime
from frappe.utils.data import now_datetime
from bbl_api.utils import print_blue, print_cyan, send_wechat_msg_temp_app

#todo 设定统计截至每天8点的数据， 需要放在8点之后执行
def zpl_perday(delta:int = 0):
    report_type = '日报'
    rt_str = f'<< 中频炉测温-{report_type} >>\n'
    now_time = now_datetime()
    now_time = now_time + datetime.timedelta(days=delta)
    end_time = now_time.replace(hour=8, minute=0, second=0, microsecond=0)
    start_time = end_time + datetime.timedelta(days=-1)
    # start_time = start_time.replace(hour=20, minute=0, second=0, microsecond=0)
    
    msg = f"开始: {start_time}\n截止: {end_time}\n"
    rt_str += msg
    # msg = f"中频炉日报\n"  + msg
    # print_cyan(msg)
    # send_wechat_msg_admin_site(msg)
    
    # 获取中频炉设备列表
    doc = 'Esp Adc Base'
    li = zpl_name_list(doc, start_time, end_time)
    
    for zpl_name in li:
        rt_str += zpl_calc(doc, report_type, zpl_name, start_time, end_time)
    # print_cyan(rt_str)
    send_wechat_msg_temp_app(rt_str)


def zpl_name_list(doc, start_time, end_time):
    li = frappe.db.get_list(doc, 
                    filters =  {
                        'creation': ('between', [start_time, end_time]),
                        'op_type': 'ZPL_TEMP',
                    },
                    pluck = 'dev_name',
                    distinct = True,
                    ignore_ifnull = True)
    print_blue(li)
    return li

def zpl_record_list(doc, zpl_name, start_time, end_time):
    li = frappe.db.get_list(doc, 
                        filters =  {
                            'dev_name': zpl_name,
                            'op_type': 'ZPL_TEMP',
                            'creation': ('between', [start_time, end_time]),
                        },
                        # fields=['em_name', 'modified' ,'et', 'name'],
                        fields=['*'],
                        # order_by='for_date asc',
                        )
    return li

def zpl_calc(doc, report_type, zpl_name, start_time, end_time):
    # print_blue(f'zpl_calc: {zpl_name}')
    rt_str = f'-- {zpl_name} --\n'
    li = zpl_record_list(doc, zpl_name, start_time, end_time)
    rt_str += f'总数量: {len(li)} 根\n'
    # 计算最大值，最小值
    temp_max = max(zpl.target_top for zpl in li)
    temp_min = min(zpl.target_top for zpl in li)
    rt_str += f'最高温度: {temp_max}\n最低温度: {temp_min}\n'
    # 统计各区间温度
    temp_range = (800, 1000, 1130, 1180, 1230, 1300)
    temp_cnt_map = _zpl_range_count(li, temp_range)
    rt_str += f'温度范围统计: \n{ _zpl_map_to_str(temp_cnt_map) }\n'

    # todo 数据是否应该存入数据库
    # em_mk_report(em_name, report_type, li)
    return rt_str
    
def _zpl_range_count(li, rg_list):
    temp_cnt = {}
    for rg in rg_list:
        temp_cnt[rg] = 0
    for record in li:
        temp = record.target_top
        for rg in reversed(rg_list):
            if temp >= rg:
                temp_cnt[rg] += 1
                break
    # print_blue_pp(temp_cnt)
    return temp_cnt
    
def _zpl_map_to_str(zpl_map):
    rt_str = ''
    temp_list = list(zpl_map.keys())
    # for i in range(0, len(zpl_map)-1):
    for i in range(0, len(zpl_map)):
        key = f'{temp_list[i]:>4}度'
        i += 1
        # if i < len(zpl_map)-1:
        if i < len(zpl_map):
            key +=  f'-{temp_list[i]:>4}度:'
        else:
            key += f'-{" ":>2}以上:'
        rt_str += f'{key} {zpl_map.get(temp_list[i-1]):>5} 根\n'
    return rt_str




#   <<温度记录统计日报表>>
# 日期：2023-08-29 08:01:26  
#  ---调质1测温枪---
# 日产量：     0 根
#  ---1线中频炉测温枪---
# 日产量：   114 根
#  820度-1150度：  14 根 12.28%
# 1150度-1180度：  36 根 31.58%
# 1180度-1230度：  59 根 51.75%
# 1230度-1500度：   5 根 4.39%
#  ---2线中频炉测温枪---
# 日产量：     0 根

# temp_static = {
#     800:0,
#     1000:0,
#     1130:0,
#     1180:0,
#     1230:0,
# }
    