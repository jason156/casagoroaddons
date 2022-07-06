# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging
from datetime import timedelta
from functools import partial

import psycopg2
import pytz

from odoo import api, fields, models, tools, _
from odoo.tools import float_is_zero
from odoo.exceptions import UserError
from odoo.http import request
from odoo.addons import decimal_precision as dp

_logger = logging.getLogger(__name__)


class PosSession(models.Model):
    _inherit = "pos.session"

    temp_ids = fields.One2many('posorder.queue','session_id',string='Temporary Data')
    temp_count = fields.Integer('Pending Order', compute='_compute_pending_order')


    @api.depends('temp_ids')
    def _compute_pending_order(self):
        for session in self:
            temp_order = session.mapped('temp_ids').filtered(lambda x: x.state == 'draft')
            session.temp_count = len(temp_order)


    # @api.multi
    def action_pos_session_closing_control(self):
        self._check_pos_session_balance()
        for session in self:
            temporary_data = self.env['posorder.queue'].search([('session_id','=',session.id),('state','=','draft')],limit=1)
            if temporary_data:
                raise UserError('Session ini belum dapat di closing karena Masih ada transaksi yang belum terposting! Silakan dicoba kembali beberapa menit lagi')
            session.write({'state': 'closing_control', 'stop_at': fields.Datetime.now()})
            if not session.config_id.cash_control:
                session.action_pos_session_close()

    def action_view_temp(self):
        action = self.env.ref('pos_order_queue.action_posorder_queue_tree_all').read()[0]
        temps = self.mapped('temp_ids').filtered(lambda x: x.state == 'draft')
        tempids = []
        for temp in temps:
            tempids.append(temp.id)
        action['domain'] = [('id', 'in', tempids)]

        return action