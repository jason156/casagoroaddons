from odoo import fields, models


class posPaymentMethod(models.Model):

    _inherit = 'pos.payment.method'
    _sql_constraints = [
        ('shortcut_unique', 'unique(shortcut)', 'shortcut already exists!')
    ]

    shortcut = fields.Char(
        string='shortcut',
        size=1,
    )
