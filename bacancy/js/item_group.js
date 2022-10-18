frappe.ui.form.on("Item Group", {
    refresh(frm) {
        if (is_root(frm.doc.name)) return;
        toggle_field_property(frm);
        delete frm._all_categories;
    },

    parent_item_group(frm) {
        if (!frm.is_new()) return;
        toggle_field_property(frm);

        if (is_category(frm.doc.parent_item_group))
            frm.set_value("is_group", 1);
        else
            frappe.db.get_value(
                "Item Group",
                frm.doc.parent_item_group,
                "pch_sc_item_series",
                (r) => {
                    frm.set_value("pch_sc_item_series", r.pch_sc_item_series);
                }
            );
    },

    async pch_sc_item_series(frm) {
        if (
            !frm.is_new() ||
            !frm.doc.pch_sc_item_series ||
            !is_category(frm.doc.parent_item_group)
        )
            return;

        if (!frm._all_categories) {
            const { message } = await frappe.call({
                method: "bacancy.api.item_group.get_all_categories",
            });
            frm._all_categories = message;
        }

        frm._all_categories.forEach((r) => {
            if (r.pch_sc_item_series == frm.doc.pch_sc_item_series)
                frappe.msgprint(
                    `Item Series already used for ${r.name}.`,
                    "Duplicate Item Series"
                );
        });
    },
});

function toggle_field_property(frm) {
    const is_cat = is_category(frm.doc.parent_item_group);
    frm.toggle_reqd("parent_item_group", true);
    frm.toggle_reqd("pch_sc_item_series", is_cat);
    frm.toggle_enable(
        "pch_sc_item_series",
        is_cat && (frm.is_new() || !frm.doc.pch_sc_item_series)
    );

    frm.toggle_enable("is_group", !is_cat);
}

function is_category(parent_item_group) {
    if (!parent_item_group) return false;
    return is_root(parent_item_group);
}

function is_root(item_group) {
    return item_group === frappe.boot.root_item_group;
}
