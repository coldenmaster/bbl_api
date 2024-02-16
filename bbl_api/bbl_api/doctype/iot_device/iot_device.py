# Copyright (c) 2023, BBL and contributors
# For license information, please see license.txt

import frappe
import json
from frappe.model.document import Document

from bbl_api.utils import *
from mqtt.mqtt_rt import bbl_mqtt_client

class IotDevice(Document):
    
    def before_validate(self):
        print('IotDevice before validate')
        self.doc_change()
        
    def on_change(self):
        print('IotDevice on change')

    def doc_change(self, **kw):
        # tempHi = self.alarm_val_one
        # tempLo = self.alarm_val_two
        # self.reload()
        if (not frappe.has_permission("Iot Device", "write")):
            print_red(f'has permission: {frappe.has_permission("Iot Device", "write")}')
            return True
        # self.alarm_val_one = tempHi
        # self.alarm_val_two = tempLo
        old_doc = self.get_doc_before_save()
        
        # print_blue(f'self: {vars(self)}')
        # print_green(f'old: {vars(old_doc)}')
        # print_yellow(f'tempHi:{tempHi}  tempLo:{tempLo} | old tempHi:{old_doc.alarm_val_one}  tempLo:{old_doc.alarm_val_two}')
        if self.alarm_val_one != old_doc.alarm_val_one \
                or self.alarm_val_two != old_doc.alarm_val_two:         
            print_red(f'send mqtt to esp8266')
            topic = 'esp/in'
            msg = {
                "deviceId": self.device_id,
                "tempHigh": self.alarm_val_one,
                "tempLow": self.alarm_val_two,
            }
            bbl_mqtt_client.publish(topic, json.dumps(msg))
        else:
            print_red(f'no alarm change')
        