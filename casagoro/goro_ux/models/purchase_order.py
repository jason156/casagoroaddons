from odoo import models
import logging

_logger = logging.getLogger(__name__)


class purchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def print_pricelist(self):
        product_ids = self.mapped('order_line').mapped('product_id')
        _logger.info(product_ids)

        view_id = self.env.ref(
            'product_pricelist_direct_print.view_product_pricelist_print')

        return {
            'name': 'Pricelist',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'product.pricelist.print',
            'res_id': False,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {'active_model': 'product.product', 'active_ids': product_ids.ids},
            'view_id': view_id.id
        }
