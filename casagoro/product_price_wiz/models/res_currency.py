from odoo import fields, models


class resCurrency(models.Model):
    _inherit = 'res.currency'

    def bulk_price_update(self):
        supplierinfo_ids = self.env['product.supplierinfo'].search([
            ('currency_id', '=', self.id)])
        template_ids = supplierinfo_ids.mapped('product_tmpl_id')
        template_ids.update_prices()