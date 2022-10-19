import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def create_fields():
    custom_fields = {
        "Item Group": [
            {
                "fieldname": "pch_sc_item_series",
                "label": "Subcategory Item Series",
                "fieldtype": "Data",
                "insert_after": "column_break_5",
                "description": "eg. RES- for RES-00001",
            },
        ]
    }

    create_custom_fields(custom_fields)
