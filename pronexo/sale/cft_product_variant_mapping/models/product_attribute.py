# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError
from odoo.osv import expression

class ProductTemplateAttributeValue(models.Model):
 
    _inherit = "product.template.attribute.value"
    
    def unlink(self):
        
        if self._context.get('variant_manager',False):
            pass
        else:
            return super(ProductTemplateAttributeValue, self).unlink()