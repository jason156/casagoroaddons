from odoo import fields, models, api
import time

class MsMagicButton(models.TransientModel):
    _name = "ms.magic.button"
    _description = "Magic Button"

    action = fields.Selection([
        ('cancel_picking_expire','Cancel Picking Expired')
    ], string="Action", default="cancel_picking_expire")

    def action_magic(self):
        if self.action == 'cancel_picking_expire' :
            self.cancel_picking_expire()

    def cancel_picking_expire(self):
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')
        picking_ids = self.env['stock.picking'].search([
            ('state','not in',['cancel','done']),
            ('scheduled_date','<',current_time)
        ])
        move_ids = picking_ids.mapped('move_ids_without_package').filtered(lambda move: move.state not in ['cancel','done'])
        move_ids._action_cancel()
