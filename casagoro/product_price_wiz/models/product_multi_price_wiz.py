from odoo import fields, models, api, _
from odoo.tools import safe_eval


import logging

_logger = logging.getLogger(__name__)


class ProductMultiPriceWiz(models.TransientModel):
    _name = 'product.multi_price_wiz'
    _description = 'multi price wizard'

    domain = fields.Text(
        string='Domain'
    )
    sale_price_percent = fields.Float(
        string='sale percent',
        readonly=False,
    )
    line_ids = fields.One2many(
        'product.multi_price_wiz.line',
        'wiz_id',
        string='List',
    )
    update_prices = fields.Boolean(
        'Update price',
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

    
    @api.model
    def default_get(self, fields_list):
        res = super(ProductMultiPriceWiz, self).default_get(fields_list)
        leaf = []
        if 'active_ids' in self._context:
            leaf += [('id', 'in', self._context['active_ids'])]             
            
            res.update({'domain': str(leaf)})
        return res

    def action_set_price(self):

        leaf = safe_eval(self.domain or '[]')
        product_ids = self.env['product.template']. search(leaf)
        if self.sale_price_percent:
            product_ids.default_percent = self.sale_price_percent
            product_ids.price_round = self.price_round
            product_ids.price_surcharge = self.price_surcharge
        for line in self.line_ids:
            pricelist_item = self.env['product.pricelist.item'].search([
                ('product_tmpl_id', 'in', product_ids.ids),
                ('pricelist_id', '=', line.pricelist_id.id),
                ('min_quantity', '=', line.min_quantity),
            ])
            new_rules = []
            for missing_products in pricelist_item.mapped('product_tmpl_id') - product_ids:
                new_rules.append({
                    'pricelist_id': line.pricelist_id.id,
                    'product_tmpl_id': missing_products.id,
                    'default_percent': line.default_percent,
                    'min_quantity': line.min_quantity,
                    'price_round': line.price_round,
                    'price_surcharge': price_surcharge,
                    'applied_on': '1_product'
                }) 
            if len(new_rules):    
                self.env['product.pricelist.item'].create(new_rules)             
            pricelist_item.default_percent = line.default_percent
            pricelist_item.price_round = line.price_round
            pricelist_item.price_surcharge = line.price_surcharge
        if self.update_prices:
            product_ids.update_prices()

    def action_price_wiz(self):
        active_ids = self.env.context.get('active_ids')
        if not active_ids:
            return ''

        return {
            'name': _('Margenes'),
            'res_model': 'product.multi_price_wiz',
            'view_mode': 'form',
            'view_id':  self.env.ref('product_price_wiz.product_multi_price_wiz_form').id,
            'context': {'active_ids':  active_ids},
            'target': 'new',
            'type': 'ir.actions.act_window',
        }


class ProductPriceWizLine(models.TransientModel):
    _name = 'product.multi_price_wiz.line'
    _description = 'Product price wizard line'

    wiz_id = fields.Many2one(
        'product.multi_price_wiz',
        string='wiz',
    )
    pricelist_id = fields.Many2one(
        'product.pricelist',
        string='pricelist',
    )
    default_percent = fields.Float(
        string='Default percent',
        readonly=False,
    )
    min_quantity = fields.Integer(
        string='min qty',
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
