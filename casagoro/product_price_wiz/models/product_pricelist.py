from odoo import fields, models


class ProductPricelist(models.Model):
    _inherit = 'product.pricelist'

    default_percent = fields.Float(
        string='Default percent',
        default=70.0
    )

    use_price_wiz = fields.Boolean(
        string='Use in wizard',
    )


class ProductPricelistItem(models.Model):
    _inherit = 'product.pricelist.item'

    default_percent = fields.Float(
        string='Default percent',

    )
