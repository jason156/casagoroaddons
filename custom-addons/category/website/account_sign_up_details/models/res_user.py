# -*- coding: utf-8 -*-
#################################################################################
#
# Copyright (c) 2018-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>:wink:
# See LICENSE file for full copyright and licensing details.
#################################################################################
from odoo import api, fields, models, _
import logging

_logger = logging.getLogger(__name__)

class ResUsers(models.Model):
	_inherit = 'res.users'

	@api.model
	def signup(self, values, token=None):
		""" signup a user, to either:
			- create a new user (no token), or
			- create a user for a partner (with token, but no user for partner), or
			- change the password of a user (with token, and existing user).
			:param values: a dictionary with field values that are written on user
			:param token: signup token (optional)
			:return: (dbname, login, password) for the signed up user
		"""
		
		if token:
			partner = self.env['res.partner']._signup_retrieve_partner(token, check_validity=True, raise_exception=True)
			partner_user = partner.user_ids and partner.user_ids[0] or False
			if partner_user:

				values['wk_dob'] = values.get('wk_dob')
		else:
			
			values['wk_dob'] = values.get('wk_dob')
		return super(ResUsers, self).signup(values, token)