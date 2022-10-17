import frappe

from frappe.desk.treeview import get_children
from frappe.utils.nestedset import get_root_of


@frappe.whitelist()
def get_item_group_properties(doc):
    doc = frappe.parse_json(doc)
    out = {"is_category": is_category(doc.parent_item_group)}

    if out["is_category"]:
        out["all_categories"] = get_all_categories()
    else:
        out["category_item_series"] = get_category_item_series(doc.parent_item_group)

    return out


def is_category(parent_item_group):
    if not parent_item_group:
        return False

    return is_root(parent_item_group)


def is_root(item_group):
    return item_group == get_root_of("Item Group")


def get_category_item_series(item_group):
    return frappe.db.get_value("Item Group", item_group, "pch_sc_item_series")


def get_all_categories():
    root = get_root_of("Item Group")
    categories = [x.get("value") for x in get_children("Item Group", root)]

    return frappe.get_list("Item Group", filters={"name": ["in", categories]}, fields=["name" ,"pch_sc_item_series"])