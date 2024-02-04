# Copyright (c) 2023, BBL and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.query_builder import DocType, Interval
from frappe.query_builder.functions import Now

class IPInfo(Document):
	@staticmethod
	def clear_old_logs(days=None):
		if not days:
			days = 90
		doctype = DocType("IP Info")
		frappe.db.delete(doctype, filters=(doctype.modified < (Now() - Interval(days=days))))
