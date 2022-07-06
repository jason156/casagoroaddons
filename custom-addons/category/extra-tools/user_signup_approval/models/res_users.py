# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright 2019 Odoo IT now <http://www.odooitnow.com/>
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

import werkzeug
from odoo import models, fields, api, _


class Users(models.Model):
    _inherit = "res.users"

    approved_user = fields.Boolean('Approved User ?')
    rejected_user = fields.Boolean('Rejected User ?')
    tax_no = fields.Char('Tax Identification Number')
    cust_name = fields.Char('Customer Name')
    company_id_file = fields.Binary('Company ID')
    company_id_filename = fields.Char('Company ID FileName')
    letter_intent = fields.Binary('Letter Intent')
    letter_intent_filename = fields.Char('Letter Intent Filename')
    board_resolution = fields.Binary('Board Resolution')
    board_resolution_filename = fields.Char('Board Resolution Filename')
    user_firstname = fields.Char('First Name')
    user_lastname = fields.Char('Last Name')
    user_city = fields.Char('City')
    user_country_id = fields.Many2one('res.country', 'Country')
    user_phone = fields.Char('Phone')

    def _compute_state(self):
        for user in self:
            user.state = 'active' if user.login_date and user.active else 'new'

    def approve_user(self):
        self.ensure_one()
        self.write({'active': True,
                    'approved_user': True,
                    'rejected_user': False,
                    'state': 'active'})
        self.partner_id.active = True
        template = self.env.ref('user_signup_approval.mail_template_user_signup_account_created', raise_if_not_found=False)
        if template:
            template.sudo().with_context(
                lang=self.lang,
                auth_login=werkzeug.url_encode({'auth_login': self.login}),
                password=self.password
            ).send_mail(self.id, force_send=True)

    def reject_user(self):
        self.ensure_one()
        self.write({'active': False,
                    'approved_user': False,
                    'rejected_user': True,
                    'state': 'new'})
        self.partner_id.active = False
        template = self.env.ref('user_signup_approval.mail_template_user_signup_account_rejected', raise_if_not_found=False)
        if template:
            template.sudo().send_mail(self.id, force_send=True)
