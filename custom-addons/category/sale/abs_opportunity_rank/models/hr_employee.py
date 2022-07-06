# -*- coding: utf-8 -*-
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2020-today Ascetic Business Solution <www.asceticbs.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#################################################################################
from odoo import api, fields, models, _

## inherit class 'hr.employee' to get details of employee and set rank according to assigned Opportunity to salesperson
class Employee(models.Model):
    _inherit = "hr.employee"

    number_opportunity_rank = fields.Integer(string="Rank", compute='opportunity_rank')
    amount_opportunity_rank = fields.Float(string="Amount")

    def opportunity_rank(self):
        employee_rank_list = []
        for employee in self:
            if employee.number_opportunity_rank:
                continue
            else: 
                if employee.user_id or employee.number_opportunity_rank:
                    opportunity_list = []
                    total_amount = 0
                    opportunity_ids = self.env['crm.lead'].search([('user_id','=',employee.user_id.id)])
                    if opportunity_ids:
                        for opportunity in opportunity_ids:
                            opportunity_list.append(opportunity)
                            total_amount = total_amount + opportunity.planned_revenue
                        employee_dict = { 'employee' : employee,'length' : len(opportunity_list),'total_amount' : total_amount}
                        employee_rank_list.append(employee_dict)

                    if employee_rank_list:
                        ## sorted dictionary to get rank of employee
                        newlist = sorted(employee_rank_list, key=lambda k: k['length'], reverse=True)
                        rank = 0
                        for line in newlist:
                            if line:
                                rank = rank + 1
                                line['employee'].update({'number_opportunity_rank' : rank})
                                line['employee'].write({'amount_opportunity_rank' : line['total_amount']})
                else:
                    employee.number_opportunity_rank = 0
                    employee.amount_opportunity_rank = 0
