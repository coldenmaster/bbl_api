from frappe import _

from bbl_api.utils import print_purple

def get_data():
    print_purple("I am config.desktop")
    
    return [
		{
			"module_name": "Bbl Api",
			"type": "module",
			"label": _("Bbl Api")
		}
	]
