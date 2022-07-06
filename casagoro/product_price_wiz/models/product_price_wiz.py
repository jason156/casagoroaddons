from odoo import fields, models, api
import logging

_logger = logging.getLogger(__name__)


class ProductPriceWiz(models.TransientModel):
    _name = 'product.price_wiz'
    _description = 'Product price wizard'

    product_id = fields.Many2one(
        'product.template',
        string='Products',
    )
    seller_price = fields.Float(
        string='Seller price',

    )
    sale_price_percent = fields.Float(
        string='sale percent',
        related='product_id.default_percent',
        readonly=False,
    )
    list_price = fields.Float(
        string='List price',
        related='product_id.list_price',
        readonly=False,
    )
    actual_price = fields.Float(
        string='Actual',
        readonly=True,
    )

    line_ids = fields.One2many(
        'product.price_wiz.line',
        'wiz_id',
        string='fields',
    )

    @api.onchange('sale_price_percent')
    def _onchange_sale_price_percent(self):
        if 'no_update_listprice' not in self.env.context:
            self.list_price = self.seller_price * \
                (1.0 + (self.sale_price_percent / 100))

    @api.onchange('list_price')
    def _onchange_list_price(self):
        self.with_context(no_update_listprice=True).sale_price_percent = (
            (self.list_price / self.seller_price) - 1) * 100
        if self.sale_price_percent < 1.0:
            return {'warning': {'title': 'Error en el porcentaje',
                                'message': 'El precio de venta es menor al de compra'}}

    @api.model
    def default_get(self, fields_list):
        res = super(ProductPriceWiz, self).default_get(fields_list)

        product_id = self.env["product.template"].browse(
            self.env.context["default_product_id"])
        product_id.add_default_listprice()

        res['actual_price'] = product_id.list_price
        res['sale_price_percent'] = product_id.default_percent and product_id.default_percent or 70.0
        if len(product_id.seller_ids):
            if product_id.currency_id.id != product_id.seller_ids[0].currency_id.id:

                net_price = product_id.seller_ids[0].currency_id._convert(
                    product_id.seller_ids[0].net_price,
                    product_id.currency_id,
                    self.env.company,
                    fields.Date.today()
                )
            else:
                net_price = product_id.seller_ids[0].net_price

            res['seller_price'] = product_id.supplier_taxes_id.compute_all(
                net_price,
                product_id.currency_id,
                1.0,
                product_id,
                False
            )['total_included']
            lines = []
            item_ids = self.env['product.pricelist.item'].search(
                [('product_tmpl_id', '=', product_id.id)])
            for item in item_ids:
                actual_price = item.fixed_price
                if product_id.seller_ids[0].currency_id.id != item.pricelist_id.currency_id.id:
                    seller_price = product_id.currency_id._convert(
                        res['seller_price'],
                        item.pricelist_id.currency_id,
                        self.env.company,
                        fields.Date.today()
                    )
                else:
                    seller_price = res['seller_price']
                default_percent = item.default_percent if item.default_percent > 0 else item.pricelist_id.default_percent

                fixed_price = seller_price * \
                    (1.0 + (default_percent / 100))

                lines.append([0, 0, {'pricelist_item_id': item.id,
                                     'default_percent': default_percent,
                                     'pricelist_id': item.pricelist_id.id,
                                     'min_quantity': item.min_quantity,
                                     'actual_price': actual_price,
                                     'fixed_price': fixed_price,
                                     }])

            res['line_ids'] = lines
        return res

    def action_dummie(self):

        return

    def action_add_missing_list(self):
        item_ids = self.env['product.pricelist.item'].search(
            [('product_tmpl_id', '=', self.product_id.id)]).mapped('pricelist_id')
        list_ids = self.env['product.pricelist'].search(
            [('use_price_wiz', '=', True)])
        missing = list_ids - item_ids
        for pricelist in missing:
            self.env['product.pricelist.item'].create({
                'pricelist_id': pricelist.id,
                'product_tmpl_id': self.product_id.id,
                'default_percent': pricelist.default_percent,
                'applied_on': '1_product'
            })
        self.name = "New name"

        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'product.price_wiz',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': self.env.context,
        }


class ProductPriceWizLine(models.TransientModel):
    _name = 'product.price_wiz.line'
    _description = 'Product price wizard line'

    wiz_id = fields.Many2one(
        'product.price_wiz',
        string='wiz',
    )
    seller_price = fields.Float(
        string='Seller price',
        related='wiz_id.seller_price'
    )

    pricelist_item_id = fields.Many2one(
        'product.pricelist.item',
        string='item',
    )
    pricelist_id = fields.Many2one(
        'product.pricelist',
        string='pricelist',
        related='pricelist_item_id.pricelist_id'
    )
    default_percent = fields.Float(
        string='Default percent',
        related='pricelist_item_id.default_percent',
        readonly=False,
    )
    min_quantity = fields.Integer(
        string='min qty',
        related='pricelist_item_id.min_quantity'
    )
    fixed_price = fields.Float(
        string='Price',
        related='pricelist_item_id.fixed_price',
        readonly=False,
    )
    actual_price = fields.Float(
        string='actual',
        readonly=True,
    )

    @api.onchange('default_percent')
    def _onchange_sale_price_percent(self):
        for line in self:
            line.fixed_price = line.seller_price * \
                (1.0 + (line.default_percent / 100))

    @api.onchange('fixed_price')
    def _onchange_fixed_price(self):
        show_warn = False
        for line in self:
            line.default_percent = (
                (line.fixed_price / line.seller_price) - 1) * 100
            if line.default_percent < 1.0:
                show_warn = True

        if show_warn:
            return {'warning': {'title': 'Error en el porcentaje',
                                'message': 'El precio de venta es menor al de compra'}}
