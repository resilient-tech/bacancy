import frappe
from frappe.utils.nestedset import get_root_of


def set_bootinfo(bootinfo):
    bootinfo["root_item_group"] = get_root_of("Item Group")
