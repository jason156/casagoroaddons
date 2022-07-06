from odoo import fields, models, api
from odoo.tools.safe_eval import safe_eval


class PosUnpublish(models.TransientModel):
    _name = 'pos.unpublish'
    _description = 'pos unpublish'

    create_window = fields.Date(
        string='Creados antes de',
        required=True
    )

    last_purchase = fields.Date(
        string='Ultima compra anterior a',
        required=True
    )

    last_sale = fields.Date(
        string='Ultima venta anterior a',
        required=True
    )

    no_has_stock = fields.Boolean(
        string='sin Stock',
        default=True,
    )
    domain = fields.Char(
        string='Domain',
        compute='compute_domain'
    )

    @api.depends('create_window', 'last_purchase', 'last_sale', 'no_has_stock')
    def compute_domain(self):
        if not self.create_window or not self.last_purchase or not self.last_sale:
            self.domain = [('id', '=', False)]
            return
        query = """SELECT pp.id 
                from product_product pp
                join product_template pt on pt.id = pp.product_tmpl_id
                left join purchase_order_line pul on pul.product_id = pp.id
                left join pos_order_line posl on posl.product_id = pp.id
                where pp.create_date <= '%s' and 
                    pt.available_in_pos = True
                group by pp.id, pp.create_date, pt.available_in_pos
                    having (max(pul.create_date) <= '%s' or max(pul.create_date) is Null) 
                    and (max(posl.create_date) <= '%s' or max(posl.create_date) is Null) 
                    """ % (self.create_window,
                           self.last_purchase,
                           self.last_sale)
        self._cr.execute(query)

        ids = [x['id'] for x in self._cr.dictfetchall()]
        domain = [('id', 'in', ids)]
        if self.no_has_stock:
            domain.append(('qty_available', '<=', 0))

        self.domain = domain

    def action_unpublish(self):
        self.compute_domain()
        domain = safe_eval(self.domain)
        self.env['product.product'].search(
            domain).write({'available_in_pos': False})
