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
from odoo import api, fields, models,_

#create a new class for MultipleProductPurchase. 
class MultipleProductPurchase(models.TransientModel):
    _name = "multiple.product.purchase"
    _description = "Multiple Product Purchase"

    product_ids = fields.Many2many('product.product',string="Products")

    def add_multiple_product_purchase(self):
        order_line_obj = self.env['purchase.order.line']  
        if self.env.context.get('active_model')=='purchase.order': 
            active_id = self.env.context.get('active_id',False)
            order_id = self.env['purchase.order'].search([('id', '=', active_id)]) 
            if order_id and self.product_ids: 
                for record in self.product_ids:
                    if record:
                        tax_list = []  
                        for tax in record.supplier_taxes_id:
                            if tax:
                                tax_line = self.env['account.tax'].search([('id','=',tax.id)]) 
                                if tax_line:
                                    tax_list.append(tax.id)               
                        order_line_dict ={
                                  'order_id':order_id.id,
                                  'product_id':record.id,
                                  'product_uom':record.uom_id.id, 
                                  'price_unit':record.standard_price,  
                                  'date_planned':fields.Datetime.now(),
                                  'product_qty':1.00,
                                  'name':record.name,
                                  'taxes_id':[(6,0,tax_list)]
                                  }          
                        order_line_obj.create(order_line_dict)
