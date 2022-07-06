from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    user_id = fields.Many2one('res.users',
                              string='Public User',
                              related='website_id.user_id',
                              readonly=False,
                              required=True
                              )
