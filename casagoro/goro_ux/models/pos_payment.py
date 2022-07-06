from odoo import fields, models


class posPayment(models.Model):
    _inherit = 'pos.payment'

    crm_team_id = fields.Many2one(
        'crm.team',
        string='Team',
        compute='compute_team',
        search='search_team',
    )

    def compute_team(self):
        for payment in self:
            if len(payment.session_id.config_id.crm_team_id):
                payment.crm_team_id = payment.session_id.config_id.crm_team_id.id

    def search_team(self, operator, value):
        return [('session_id.config_id.crm_team_id', operator, value)]
