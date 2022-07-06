from odoo import models, api
from odoo.tools.float_utils import float_round


class ProductTemplate(models.Model):

    _inherit = 'product.template'

    @api.onchange('product_brand_id')
    def _onchange_product_brand_id(self):
        if len(self.product_brand_id.public_brand_id):
            self.dr_brand_id = self.product_brand_id.public_brand_id
    
    def _get_combination_info(self, combination=False, product_id=False, add_qty=1, pricelist=False, parent_combination=False, only_template=False):
        combination_info = super(ProductTemplate, self)._get_combination_info(
            combination=combination, product_id=product_id, add_qty=add_qty, pricelist=pricelist,
            parent_combination=parent_combination, only_template=only_template)

        if combination_info['product_id']:
            product = self.env['product.product'].sudo().browse(combination_info['product_id'])
            website = self.env['website'].get_current_website()
            if website:
                product = product.with_context(warehouse=website.warehouse_id.id)
                rounding = product.uom_id.rounding

                combination_info['virtual_available'] = float_round(
                    product.qty_available - product.incoming_qty,
                    precision_rounding=rounding)

        return combination_info
