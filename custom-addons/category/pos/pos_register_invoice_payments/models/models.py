# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   License URL : <https://store.webkul.com/license.html/>
# 
#################################################################################
from odoo import api, fields, models
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
	_inherit = "account.move"

	@api.model
	def wk_register_invoice_payment(self,kwargs):
		if(kwargs.get('invoice_id')):
			invoice = self.browse(kwargs.get('invoice_id'))			
			payment_id = self.env['account.payment'].create({
				'partner_type': 'customer', 
				'amount': kwargs.get('amount'), 
				'has_invoices': True, 
				'payment_method_id': 1,
				'invoice_ids': [invoice.id],
				'payment_type': 'inbound', 
				'payment_method_code': 'manual',
				'communication': kwargs.get('payment_memo') or '',
				'partner_id': invoice.partner_id.id,
				'journal_id': kwargs.get('journal_id'), 
				'currency_id': invoice.currency_id.id,
			})			
			if payment_id:
				payment_id.post()
			return {
				'residual':invoice.amount_residual,
				'state':invoice.state
			}

	def wk_assign_outstanding_credit(self, line_id):
		self.ensure_one()
		lines = self.env['account.move.line'].browse(line_id)
		lines += self.line_ids.filtered(lambda line: line.account_id == lines[0].account_id and not line.reconciled)
		wk_register = lines.reconcile()
		if(wk_register):
			return self.read(['invoice_outstanding_credits_debits_widget','invoice_payments_widget','state','amount_total','amount_residual'])
		else:
			return False


	@api.model
	def enable_accounting_group(self):
		try:
			self.env.ref('account.group_account_user').write({'users' : [(4, self.env.ref('base.user_admin').id)]})	
		except Exception as e:
			_logger.info("*****************Exception**************",e)
