frappe.ui.form.on("Item Group", {
    onload(frm) {
        if (frm.is_new()) frm.set_df_property("parent_item_group", "reqd", 1);
        else frm.set_df_property("pch_sc_item_series", "read_only", 1);
    },

    refresh(frm) {
        if (!frm._item_group_properties?.[frm.doc.name])
            update_item_group_properties(frm);
    },

    parent_item_group: update_item_group_properties,

    pch_sc_item_series(frm) {
        if (!frm.doc.pch_sc_item_series) return;
        const properties = frm._item_group_properties[frm.doc.name];

        if (!properties.is_category) return;
        properties.all_categories.forEach((r) => {
            if (r.pch_sc_item_series == frm.doc.pch_sc_item_series)
                frappe.msgprint(
                    `Item Series already used for ${r.name}.`,
                    "Duplicate Item Series"
                );
        });
    },

    validate(frm) {
        frm.doc._item_group_properties = frm._item_group_properties;
    },
});

async function update_item_group_properties(frm) {
    if (!frm.doc.parent_item_group) return;

    const { message } = await frappe.call({
        method: "bacancy.api.item_group.get_item_group_properties",
        args: {
            doc: frm.doc,
        },
    });

    frm._item_group_properties = { [frm.doc.name]: message };
    update_field_property(frm, message);
}

function update_field_property(frm, properties) {
    const is_group = frm.get_field("is_group");
    const item_series = frm.get_field("pch_sc_item_series");

    if (properties.is_category) {
        is_group.df.read_only = 1;
        item_series.df.read_only = 0;
        item_series.df.reqd = 1;
        if (frm.is_new()) {
            item_series.set_value("");
            is_group.set_value(1);
        }
    } else {
        is_group.df.read_only = 0;
        item_series.df.read_only = 1;
        item_series.df.reqd = 0;
        if (frm.is_new())
            item_series.set_value(properties.category_item_series);
    }

    frm.refresh_fields();
}
