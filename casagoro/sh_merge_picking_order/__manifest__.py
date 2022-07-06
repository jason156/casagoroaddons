# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Merge Picking Orders",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "license": "OPL-1",
    "support": "support@softhealer.com",
    "category": "Warehouse",
    "summary": "Merge Picking, Merge Pickings, Merge Incoming Orders, Merge Incoming Order, Merge Delivery Order, Merge Delivery Orders, Append Picking Order, Combine Delivery Order, Combine Incoming Order, Combine Picking Orders, Combine Picking Odoo",
    "description": """This module useful to merge picking orders. Some times required to make a single order from the multiple picking orders. You can merge picking orders which are only in the draft/ waiting/ ready state. Your picking orders must have the same operation type (incoming order/delivery order) for merge orders. You can merge picking orders with many options. Merge picking orders notification comes into the chatter!""",
    "version": "13.0.3",
    "depends": [
        "stock",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/res_config_setting.xml",
        "wizard/merge_picking_order.xml",
    ],
    "images": ["static/description/background.png", ],
    "auto_install": False,
    "application": True,
    "installable": True,
    "price": 25,
    "currency": "EUR"
}
