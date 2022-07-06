# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class ProductProduct(models.Model):
    
    _inherit = 'product.product'
    
    def unlink(self):
        if self._context.get('variant_manager',False) or self._context.get('attribute_manager',False):
            return True
        else:
            return super(ProductProduct, self).unlink()
    