from __future__ import unicode_literals
import frappe
from datetime import datetime,date
from datetime import datetime

@frappe.whitelist()
def add_series_to_naming_series(pch_sc_item_series):
    arr = ['-']
    for i in arr:
        if i in pch_sc_item_series:
            print("True")
        else:
            pch_sc_item_series = pch_sc_item_series+'-'
            print("False",pch_sc_item_series)
    doc=frappe.get_doc("Naming Series")
    print("doc.set_options",doc.set_options)
    series = doc.set_options
    options1 = series.split("\n")
    print("options......1",options1)
    if pch_sc_item_series in series:
        print("element exist")
        pass
    else:
        print("element not exist")
        print("pch_sc_item_series",pch_sc_item_series)
        my_list = options1
        my_final_list1 = set(my_list)
        print(list(my_final_list1))
        my_final_list = list(my_final_list1)
        my_final_list.append(pch_sc_item_series)
        print("options....2",my_final_list)
        doc.set_series_for("Item",my_final_list)
        doc.save()
        frappe.db.commit()
    
@frappe.whitelist()
def allow_single_series(pch_sc_item_series):
    print("....................")
    print("name of first series ...........",pch_sc_item_series)
    details_First=frappe.db.sql("""select pch_sc_item_series from `tabItem Group`""", as_dict=1)
    print("parent first details",details_First)
    value = pch_sc_item_series
    list_of_all_values = [value for elem in details_First 
    for value in elem.values()]
    if value in list_of_all_values:
        frappe.msgprint("This series is already Exist")
        return value
    else:
        frappe.msgprint("This series already not Exist")