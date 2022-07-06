# -*- coding: utf-8 -*-
from odoo import _, api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_pack = fields.Boolean(
    )
    packed_product_ids = fields.Many2many(
        comodel_name='product.product',
        relation='pack_product_rel',
        column1='pack_id',
        column2='product_id',
    )
    max_items_to_select = fields.Integer(
    )
