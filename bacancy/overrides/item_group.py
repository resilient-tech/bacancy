import frappe

from frappe.utils.nestedset import get_root_of, get_descendants_of
from bacancy.api.item_group import is_root, get_category, get_item_group_properties


def onload(doc, method=None):
    doc.set_onload("root_item_group", get_root_of("Item Group"))


def validate(doc, method=None):
    if is_root(doc.name):
        return

    properties = get_item_group_properties(doc)
    validate_is_group(doc, properties)
    validate_parent_item_group(doc)
    validate_item_series(doc, properties)

    update_naming_series(doc.pch_sc_item_series)

    if properties.get("all_categories"):
        update_all_item_groups(doc)


def validate_is_group(doc, properties):
    if not doc.is_group and properties.get("is_category"):
        frappe.throw(
            "Item Group {0} is a category and should be a Group Node.".format(doc.name)
        )


def validate_parent_item_group(doc):
    if not doc.parent_item_group:
        frappe.throw(
            "Parent Item Group is Mandatory Field.", title="Missing Mandatory Field"
        )

    # Allow change in parent only if category stays same
    if _has_value_changed(doc, "parent_item_group") and get_category(
        doc.parent_item_group
    ) != get_category(doc.get_doc_before_save().parent_item_group):
        frappe.throw(
            "Parent Item Group cannot be changed to have different Category.",
            title="Validation Error",
        )


def validate_item_series(doc, properties):
    if not doc.pch_sc_item_series:
        frappe.throw(
            "Sub Category Item Series is a Mandatory Field.",
            title="Missing Mandatory Field",
        )

    # series should be same as that of category
    if (
        series := properties.get("category_item_series")
    ) and doc.pch_sc_item_series != series:
        frappe.throw(
            "Sub Category Item Series should be same as that of Parent {0}.".format(
                doc.parent_item_group
            ),
            title="Invalid Item Series",
        )

    # series should be unique for new category
    elif all_categories := properties.get("all_categories"):
        for category in all_categories:
            if (
                category.get("pch_sc_item_series") != doc.pch_sc_item_series
                or category.get("name") == doc.name
            ):
                continue

            frappe.throw(
                "Sub Category Item Series should be unique. {0} is already using {1}.".format(
                    category.get("name"), doc.pch_sc_item_series
                ),
                title="Invalid Item Series",
            )

    # change of series not allowed
    if _has_value_changed(doc, "pch_sc_item_series"):
        frappe.throw(
            "Sub Category Item Series cannot be changed.", title="Validation Error"
        )


def update_naming_series(item_series):
    naming_series = frappe.get_doc("Naming Series")
    series_list = naming_series.get_options("Item").split("\n")

    if item_series in series_list:
        return

    series_list.append(item_series)
    naming_series.set_series_for("Item", series_list)


def update_all_item_groups(doc):
    "Helper function to update all decendents when first set."

    if not doc.get_doc_before_save():
        return

    item_groups = get_descendants_of("Item Group", doc.name)
    if not item_groups:
        return

    item_group_table = frappe.qb.DocType("Item Group")
    (
        frappe.qb.update(item_group_table)
        .set(item_group_table.pch_sc_item_series, doc.pch_sc_item_series)
        .where(item_group_table.name.isin(item_groups))
        .run()
    )


def _has_value_changed(doc, field):
    "Check for change in old value only if already available"

    old = doc.get_doc_before_save()
    return old.get(field) != doc.get(field) if old and old.get(field) else False
