from odoo import fields, models, api


class productBrand(models.Model):
    _inherit = 'product.brand'

    public_brand_id = fields.Many2one(
        'dr.product.brand',
        string='public brand',
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'public_brand_id' not in vals:
                public_categ_id = self.env['dr.product.brand'].create({
                    'name': vals['name'],
                    'image': vals['logo']
                })
                vals['public_brand_id'] = public_categ_id.id
        return super().create(vals_list)

    def write(self, vals):
        records = super().write(vals)
        for record in self:
            if 'name' in vals and len(record.public_brand_id):
                record.public_brand_id = vals['name']
            if 'logo' in vals and len(record.public_brand_id):
                record.image = vals['logo']
        return records
