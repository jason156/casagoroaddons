# -*- coding: utf-8 -*-
#################################################################################
# Author      : Acespritech Solutions Pvt. Ltd. (<www.acespritech.com>)
# Copyright(c): 2012-Present Acespritech Solutions Pvt. Ltd.
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################

from openerp import models, fields, api, _

class ResUsers(models.Model):
    _inherit = "res.users"

    can_give_discount = fields.Boolean("Can Give Discount")
    can_change_price = fields.Boolean("Can Change Price")
    discount_limit = fields.Float("Discount Limit")
    based_on = fields.Selection([('pin','Pin'),('barcode','Barcode')],
                                   default='barcode',string="Authenticaion Based On")


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    @api.model
    def get_user_pin(self,user_ids):
        employee_data = False
        fields = ['pin','user_id']
        employee_data = self.sudo().search_read([('user_id','in',user_ids)],fields)
        return employee_data

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: