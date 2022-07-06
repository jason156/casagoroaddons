# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging
from datetime import datetime,timedelta
from functools import partial
import dateutil.parser

import psycopg2
import pytz

from odoo import api, fields, models, tools, _
from odoo.tools import float_is_zero
from odoo.exceptions import UserError
from odoo.http import request
from odoo.addons import decimal_precision as dp

import json

_logger = logging.getLogger(__name__)


class PosOrder(models.Model):
    _inherit = "pos.order"


    @api.model
    def create_from_ui(self, orders, draft=False):
        # Keep only new orders
        submitted_references = [o['data']['name'] for o in orders]
        print(submitted_references)
        pos_order = self.env['posorder.queue'].search([('order_ref', 'in', submitted_references)])
        orders_to_save = [o for o in orders if o['data']['name'] not in pos_order]
        order_ids = []
        _logger.info(orders_to_save)
        for tmp_order in orders_to_save:
            e_posorder = self.env['posorder.queue'].sudo().search([('order_ref','=',tmp_order['data']['name'])])
            if not e_posorder:
                pos_session = self.env['pos.session'].browse(pos_order.session_id.id)
                if pos_session.state == 'closing_control' or pos_session.state == 'closed':
                    pos_order['pos_session_id'] = self._get_valid_session(pos_order).id

                order = tmp_order['data']
                tmp_pos_order = self.env['posorder.queue'].sudo().create({
                    'jsondata': json.dumps(tmp_order),
                    'session_id':   order['pos_session_id'],
                    'order_ref':   order['name']
                })

                order_ids.append(tmp_pos_order.id)
            else:
                order_ids.append(e_posorder.id)
        

        return order_ids

    @api.model
    def _order_fields(self, ui_order):
        process_line = partial(self.env['pos.order.line']._order_line_fields, session_id=ui_order['pos_session_id'])
        userdata = self.env['res.users'].sudo().search([('id','=',ui_order['user_id'])],limit=1)
        date_order_data = dateutil.parser.isoparse(ui_order['creation_date']).strftime('%Y-%m-%d %H:%M:%S') #datetime.strptime(ui_order['creation_date'],'%Y-%m-%d-%H-%M-%S-%Z')
        return {
            'name':         ui_order['name'],
            'user_id':      ui_order['user_id'] or False,
            'session_id':   ui_order['pos_session_id'],
            'lines':        [process_line(l) for l in ui_order['lines']] if ui_order['lines'] else False,
            'pos_reference': ui_order['name'],
            'partner_id':   ui_order['partner_id'] or False,
            'date_order':   date_order_data,
            'fiscal_position_id': ui_order['fiscal_position_id'],
            'pricelist_id': ui_order['pricelist_id'],
            'amount_paid':  ui_order['amount_paid'],
            'amount_total':  ui_order['amount_total'],
            'amount_tax':  ui_order['amount_tax'],
            'amount_return':  ui_order['amount_return'],
        }

    # @api.model
    # def _process_order(self, pos_order):
    #     pos_session = self.env['pos.session'].browse(pos_order['pos_session_id'])
    #     if pos_session.state == 'closing_control' or pos_session.state == 'closed':
    #         pos_order['pos_session_id'] = self._get_valid_session(pos_order).id

    #     if self.env.user.has_group('base.group_system'):
    #         _logger.info('CREATE POS BY SCHEDULER')
    #         order = self.sudo().create(self._order_fields(pos_order))
    #     else:
    #         order = self.create(self._order_fields(pos_order))
    #     prec_acc = order.pricelist_id.currency_id.decimal_places
    #     journal_ids = set()
    #     for payments in pos_order['statement_ids']:
    #         if not float_is_zero(payments[2]['amount'], precision_digits=prec_acc):
    #             order.add_payment(self._payment_fields(payments[2]))
    #         journal_ids.add(payments[2]['journal_id'])

    #     if pos_session.sequence_number <= pos_order['sequence_number']:
    #         pos_session.write({'sequence_number': pos_order['sequence_number'] + 1})
    #         pos_session.refresh()

    #     if not float_is_zero(pos_order['amount_return'], prec_acc):
    #         cash_journal_id = pos_session.cash_journal_id.id
    #         if not cash_journal_id:
    #             # Select for change one of the cash journals used in this
    #             # payment
    #             cash_journal = self.env['account.journal'].search([
    #                 ('type', '=', 'cash'),
    #                 ('id', 'in', list(journal_ids)),
    #             ], limit=1)
    #             if not cash_journal:
    #                 # If none, select for change one of the cash journals of the POS
    #                 # This is used for example when a customer pays by credit card
    #                 # an amount higher than total amount of the order and gets cash back
    #                 cash_journal = [statement.journal_id for statement in pos_session.statement_ids if statement.journal_id.type == 'cash']
    #                 if not cash_journal:
    #                     raise UserError(_("No cash statement found for this session. Unable to record returned cash."))
    #             cash_journal_id = cash_journal[0].id
    #         order.add_payment({
    #             'amount': -pos_order['amount_return'],
    #             'payment_date': fields.Date.context_today(self),
    #             'payment_name': _('return'),
    #             'journal': cash_journal_id,
    #         })
    #     return order


class TmpPosOrder(models.Model):
    _name = 'posorder.queue'
    _order = 'id desc'

    session_id = fields.Many2one('pos.session', 'Session')
    order_id = fields.Many2one('pos.order', 'Order')
    order_ref = fields.Char('Order Ref')
    jsondata = fields.Text('JsonData')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
        ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')

    def process_json_ui(self):
        for posorder in self:
            if posorder.jsondata:
                posorder_obj = self.env['pos.order']
                orderjson = json.loads(posorder.jsondata)

                submitted_references = [orderjson['data']['name']]
                pos_order = posorder_obj.search([('pos_reference', 'in', submitted_references)])
                existing_orders = pos_order.read(['pos_reference'])
                existing_references = set([o['pos_reference'] for o in existing_orders])
                orders_to_save = []
                if orderjson['data']['name'] not in existing_references:
                    # orders_to_save = [o for o in orderjson if orderjson['data']['name'] not in existing_references]
                    orders_to_save.append(orderjson)

                order_ids = []

                for tmp_order in orders_to_save:
                    to_invoice = tmp_order['to_invoice'] or tmp_order['data'].get('to_invoice')
                    
                    existing_order = False
                    if 'server_id' in tmp_order['data']:
                        existing_order = self.env['pos.order'].search(['|', ('id', '=', tmp_order['data']['server_id']), ('pos_reference', '=', tmp_order['data']['name'])], limit=1)

                    order = tmp_order['data']
                    if to_invoice:
                        posorder_obj._match_payment_to_invoice(order)
                    pos_order = posorder_obj._process_order(tmp_order,False,existing_order)
                    print(pos_order)
                    order_ids.append(pos_order)

                    try:
                        pos_order.action_pos_order_paid()
                    except psycopg2.DatabaseError:
                        # do not hide transactional errors, the order(s) won't be saved!
                        raise
                    except Exception as e:
                        _logger.error('Could not fully process the POS Order: %s', tools.ustr(e), exc_info=True)

                    if to_invoice:
                        pos_order.action_pos_order_invoice()
                        pos_order.invoice_id.sudo().with_context(
                            force_company=self.env.user.company_id.id, pos_picking_id=pos_order.picking_id
                        ).action_invoice_open()
                        pos_order.account_move = pos_order.invoice_id.move_id

                self.write({'state' : 'done'})

    def posorder_auto_post(self,limit):
        unposted_view = self.search([('state','=','draft')],limit=limit, order='create_date')
        if unposted_view:
            for posorder in unposted_view:
                usr = self.env['res.users'].sudo().search([('id','=',posorder.session_id.user_id.id)],limit=1)
                posorder.sudo(usr).process_json_ui()


