from odoo import fields, models


class StockWarehouse(models.Model):

    _inherit = "stock.warehouse"

    intr_type_id = fields.Many2one(
        'stock.picking.type',
        string='Interdepositos',
    )
