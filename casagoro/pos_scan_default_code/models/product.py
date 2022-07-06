# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class ProductTemplate(models.Model):
    _inherit = "product.template"

    # modelo_articulo = fields.Char('Modelo Artículo')
    modelo_articulo = fields.Char(
        'Modelo Artículo', compute='_compute_modelo_articulo',
        inverse='_set_modelo_articulo', store=True)

    @api.depends('product_variant_ids', 'product_variant_ids.modelo_articulo')
    def _compute_modelo_articulo(self):
        unique_variants = self.filtered(lambda template: len(template.product_variant_ids) == 1)
        for template in unique_variants:
            template.modelo_articulo = template.product_variant_ids.modelo_articulo
        for template in (self - unique_variants):
            template.modelo_articulo = False

    def _set_modelo_articulo(self):
        for template in self:
            if len(template.product_variant_ids) == 1:
                template.product_variant_ids.modelo_articulo = template.modelo_articulo

class Product(models.Model):
    _inherit = "product.product"

    modelo_articulo = fields.Char('Modelo Artículo')


