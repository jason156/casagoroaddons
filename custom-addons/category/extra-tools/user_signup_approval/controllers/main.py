# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright 2019 Odoo IT now <http://www.odooitnow.com/>
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

import base64
import logging
import werkzeug

from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo import http, _, SUPERUSER_ID
from odoo.http import request
from odoo.addons.auth_signup.models.res_users import SignupError
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class ApproveSignupHome(AuthSignupHome):

    @http.route("/web/get_company", type='json', auth="public", website=True)
    def get_company(self, **post):
        tax_no = post.get('tin_no')
        parent_customer = request.env['res.partner'].sudo().search([('is_company', '=', True), ('vat', '=', tax_no)])
        if not parent_customer:
            raise UserError(_("TIN does not exist, Unable to proceed"))
        return parent_customer.display_name
    
    def do_signup(self, qcontext):
        """ Shared helper that creates a res.partner out of a token """
        values = { key: qcontext.get(key) for key in ('login', 'name', 'last_name', 'city', 'country_id','phone', 'password') }
        if not values:
            raise UserError(_("The form was not properly filled in."))
        values = { key: qcontext.get(key) for key in ('login', 'name', 'last_name', 'city', 'country_id','phone','tax_no','cust_name', 'password')}
        tax_no = values.get('tax_no')
        parent_customer = request.env['res.partner'].sudo().search([('is_company', '=', True), ('vat', '=', tax_no)])
        if not parent_customer:
            raise UserError(_("TIN does not exist, Unable to proceed"))
        values.update({'parent_id':parent_customer.id})
        if values.get('password') != qcontext.get('confirm_password'):
            raise UserError(_("Passwords do not match; please retype them."))
        supported_lang_codes = [code for code, _ in request.env['res.lang'].get_installed()]
        lang = request.context.get('lang', '').split('_')[0]
        if lang in supported_lang_codes:
            values['lang'] = lang
        if qcontext.get('name', False):
            values.update({'user_firstname':qcontext.get('name', False)})
        if qcontext.get('last_name', False):
            values.update({'user_lastname':qcontext.get('last_name', False)})
        if qcontext.get('city', False):
            values.update({'user_city':qcontext.get('city', False)})
        if qcontext.get('country_id', False):
            values.update({'user_country_id':qcontext.get('country_id', False)})
        if qcontext.get('phone', False):
            values.update({'user_phone':qcontext.get('phone', False)})
        if qcontext.get('company_id_file',False):
            values.update({'company_id_file':base64.encodestring(qcontext.get('company_id_file').read()),
                           'company_id_filename':qcontext.get('company_id_file').filename})
        if qcontext.get('letter_intent',False):
            values.update({'letter_intent':base64.encodestring(qcontext.get('letter_intent').read()),
                           'letter_intent_filename':qcontext.get('letter_intent').filename})
        if qcontext.get('board_resolution',False):
            values.update({'board_resolution':base64.encodestring(qcontext.get('board_resolution').read()),
                           'board_resolution_filename':qcontext.get('board_resolution').filename})
        self._signup_with_values(qcontext.get('token'), values)
        request.env.cr.commit()

    def _signup_with_values(self, token, values):
        db, login, password = request.env['res.users'].sudo().signup(values, token)
        request.env.cr.commit()  # as authenticate will use its own cursor we need to commit the current transaction
        uid = request.session.authenticate(db, login, password)
        if not uid:
            raise SignupError(_('Authentication Failed.'))
        request.session.logout(keep_db=True)

    @http.route('/web/signup', type='http', auth='public', website=True, sitemap=False)
    def web_auth_signup(self, *args, **kw):
        value = {}
        ResUser = request.env['res.users'].sudo()
        if ResUser.search([('login', '=', kw.get('login'))]):
            value['error'] = _("User is alreday registered with %s email" % (kw.get('login')))
            return request.render('auth_signup.signup', value)
        if ResUser.search([('login', '=', kw.get('login')), ('active', '=', False)]):
            value['error'] = _("User is alreday registered with %s email" % (kw.get('login')))
            return request.render('auth_signup.signup', value)
        qcontext = self.get_auth_signup_qcontext()
        if not qcontext.get('token') and not qcontext.get('signup_enabled'):
            raise werkzeug.exceptions.NotFound()
        if 'error' not in qcontext and request.httprequest.method == 'POST':
            try:
                if qcontext.get('country_id', ''):
                    qcontext.update({'country_id': int(qcontext.get('country_id'))})
                self.do_signup(qcontext)
                if qcontext.get('login', ''):
                    request.session['login'] = qcontext.get('login')
                    user_sudo = request.env['res.users'].sudo().search([('login', '=', qcontext.get('login'))])
                    user_sudo.log_ids.unlink()
                    template = request.env.ref('user_signup_approval.mail_template_new_user_signup_approval', raise_if_not_found=False)
                    admin_user = request.env['res.users'].sudo().browse(SUPERUSER_ID)
                    if template:
                        template.sudo().with_context(
                            lang=user_sudo.lang,
                            user_name=admin_user.name,
                            email_to=admin_user.email
                        ).send_mail(user_sudo.id, force_send=True)
                return werkzeug.utils.redirect('/signup/thankyou')
            except UserError as e:
                qcontext['error'] = e.name or e.value
            except (SignupError, AssertionError) as e:
                if request.env["res.users"].sudo().search([("login", "=", qcontext.get("login"))]):
                    qcontext["error"] = _("Another user is already registered using this email address.")
                else:
                    _logger.error(e)
                    qcontext['error'] = _("Could not create a new account.")
        restrict_country_ids = request.website.restrict_counrty_ids
        if restrict_country_ids:
            qcontext['country_code'] = (',').join(restrict_country_ids.mapped('code'))
        qcontext['countries'] = request.env['res.country'].sudo().search([])
        return request.render('auth_signup.signup', qcontext)

    @http.route('/signup/thankyou', auth='public', website=True, csrf=False)
    def logout(self):
        login = ''
        if request.session.get('login', ''):
            login = request.session.get('login')
        request.session.logout(keep_db=True)
        if login:
            user_sudo = request.env['res.users'].sudo().search([('login', '=', login)])
            user_sudo.write({'state': 'new',
                             'active': False,
                             'login_date': False})
            user_sudo.partner_id.write({'active': False})
        return request.render('user_signup_approval.signup_thankyou', {})
