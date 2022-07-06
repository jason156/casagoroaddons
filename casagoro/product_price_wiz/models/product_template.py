from odoo import fields, models, tools
import logging

_logger = logging.getLogger(__name__)


class ProductSupplierinfo(models.Model):

    _inherit = 'product.supplierinfo'

    def write(self, vals):
        res = super().write(vals)
        if 'price' in vals or 'net_price' in vals:
            for record in self:
                record.product_tmpl_id.price_ok = False
        return res


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    default_percent = fields.Float(
        string='Default percent',
        default=70,
    )

    price_ok = fields.Boolean(
        string='price is update',
        default=True
    )

    price_round = fields.Float(
        'Price Rounding', digits='Product Price',
        help="Sets the price so that it is a multiple of this value.\n"
             "Rounding is applied after the discount and before the surcharge.\n"
             "To have prices that end in 9.99, set rounding 10, surcharge -0.01"
    )
    price_surcharge = fields.Float(
        'Price Surcharge', digits='Product Price',
        help='Specify the fixed amount to add or substract(if negative) to the amount calculated with the discount.')

    def write(self, vals):
        res = super().write(vals)
        if 'list_price' in vals:
            self.price_ok = True
        return res

    def add_default_listprice(self):
        for product_tmpl_id in self:
            item_ids = self.env['product.pricelist.item'].search(
                [('product_tmpl_id', '=', product_tmpl_id.id)]).mapped('pricelist_id')
            list_ids = self.env['product.pricelist'].search(
                [('use_price_wiz', '=', True)])
            missing = list_ids - item_ids
            for pricelist in missing:
                self.env['product.pricelist.item'].create({
                    'pricelist_id': pricelist.id,
                    'product_tmpl_id': product_tmpl_id.id,
                    'default_percent': pricelist.default_percent,
                    'applied_on': '1_product'
                })

    def update_prices(self):
        for product_id in self:
            # product_id.add_default_listprice()
            if product_id.currency_id.id != product_id.seller_ids[0].currency_id.id:

                net_price = product_id.seller_ids[0].currency_id._convert(
                    product_id.seller_ids[0].net_price,
                    product_id.currency_id,
                    self.env.company,
                    fields.Date.today()
                )
            else:
                net_price = product_id.seller_ids[0].net_price

            seller_price = product_id.supplier_taxes_id.compute_all(
                net_price,
                product_id.currency_id,
                1.0,
                product_id,
                False
            )['total_included']
            product_price = seller_price * \
                (1.0 + (product_id.default_percent / 100))
            if product_id.price_round:
                product_price = tools.float_round(product_price, precision_rounding=product_id.price_round)
            if product_id.price_surcharge:
                product_price += product_id.price_surcharge

            product_id.list_price = product_price

            item_ids = self.env['product.pricelist.item'].search(
                [('product_tmpl_id', '=', product_id.id)])

            for item in item_ids:
                if product_id.seller_ids[0].currency_id.id != item.pricelist_id.currency_id.id:
                    seller_price = product_id.currency_id._convert(
                        seller_price,
                        item.pricelist_id.currency_id,
                        self.env.company,
                        fields.Date.today()
                    )
                else:
                    seller_price = seller_price
                default_percent = item.default_percent if item.default_percent > 0 else item.pricelist_id.default_percent
                price = seller_price * (1.0 + (default_percent / 100))
                #price = tools.float_round(price, precision_rounding=self.price_round)
                if item.price_round:
                    price = tools.float_round(
                        price, precision_rounding=item.price_round)
                if item.price_surcharge:
                    price += item.price_surcharge

                item.fixed_price = price
