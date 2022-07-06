# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class ProductTemplate(models.Model):
    
    _inherit = 'product.template'
    
    def open_variant_mapping(self):
        return {
            'type': 'ir.actions.client',
            'tag': 'variant_rearrange_screen',
            'res_id':self.id,
            'name': "Reaarange Variants"
        }
    
    @api.model
    def add_product(self,template_id=False):
        template = self.browse(int(template_id))
        if template:
            variants = []
            for variant in template.product_variant_ids:
                variants.append({
                    'name':variant.display_name,
                    'id':variant.id,
                    'attributes': [attribute.display_name for attribute in variant.product_template_attribute_value_ids]
                })
            current_template = {
                'name':template.display_name,
                'variant_count':template.product_variant_count,
                'variants': variants
            }
            value = {
            'option_id':template_id,
            'template': current_template
            }
            result = {
                'html': self.env.ref('cft_product_variant_mapping.product_template_card').render(value)
            }
            return result
        
    @api.model
    def get_html(self,template_id=False):
        templates = self.search([])
        option_list = []
        for tmpl in templates:
            option_list.append({'id':tmpl.id,'name':tmpl.display_name})
        current_template = False
        template = self.browse(template_id)
        if template:
            variants = []
            for variant in template.product_variant_ids:
                variants.append({
                    'name':variant.display_name,
                    'id':variant.id,
                    'attributes': [attribute.display_name for attribute in variant.product_template_attribute_value_ids]
                })
            current_template = {
                'name':template.display_name,
                'variant_count':template.product_variant_count,
                'variants': variants,
            }
        value = {
            'options':option_list,
            'option_id':template_id,
            'template': current_template
        }
        result = {
            'html': self.env.ref('cft_product_variant_mapping.variant_mapping').render(value)
        }
        return result

    def _create_variant_ids(self):
        if self._context.get('variant_manager',False):
            pass
        else:
            return super(ProductTemplate, self)._create_variant_ids()
    