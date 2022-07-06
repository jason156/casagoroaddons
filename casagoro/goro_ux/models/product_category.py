from odoo import fields, models, api

class productCategory(models.Model):
    _inherit = 'product.category'

    public_categ_id = fields.Many2one(
        'product.public.category',
        string='public category',
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'public_categ_id' not in vals:
                if 'parent_id' in vals:
                    parent_id = self.env['product.category'].browse(
                        vals['parent_id']).public_categ_id.id or False
                else:
                    parent_id = False

                public_categ_id = self.env['product.public.category'].create({
                    'name': vals['name'],
                    'parent_id': parent_id,
                })
                vals['public_categ_id'] = public_categ_id.id
        return super().create(vals_list)
