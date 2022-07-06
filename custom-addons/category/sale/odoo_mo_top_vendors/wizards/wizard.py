# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class Wizard(models.TransientModel):
    _name = 'odoo_mo.top_vendor'

    date_from = fields.Date(string="Date From",required=True)
    date_to = fields.Date(string="Date From",required=True)
    purchases_orders = fields.Many2many(comodel_name="purchase.order", relation="top_vendors_purchase",
                                        string="Purchase Orders")
    vendors = fields.Many2many(comodel_name="res.partner", relation="top_vendors_partner", string="Vendors",domain=[('supplier_rank','=',1)])
    no_of_vendors = fields.Integer(string="Number Of Vendors", required=True, default=1)
    lines = fields.One2many(comodel_name="odoo_mo.top_venodor_template", inverse_name="wiz_id", string="Data",
                            readonly=True)

    def _get_lines(self):
        where="date(date_approve)>=\'"+str(self.date_from)+"\'"
        where+=" and date(date_approve)<=\'"+str(self.date_to)+"\'"
        where+=" and state='purchase'"
        if self.vendors:
            if len(self.vendors)>1:
                where += " and partner_id in " + str(tuple(self.vendors.ids))
            else:
                where += " and partner_id = " + str(self.vendors.ids[0])

        if self.purchases_orders:
            if len(self.purchases_orders)>1:
                where += " and id in " + str(tuple(self.purchases_orders.ids))
            else:
                where += " and id = " + str(self.purchases_orders.ids[0])
        query = """
            select  partner_id,sum(amount_total) as amount 
            from purchase_order 
            where {where}
            group by partner_id order by amount desc
            limit {no_of_vendors}
            """.format(no_of_vendors=self.no_of_vendors,where=where)
        self._cr.execute(query)
        lines = self._cr.dictfetchall()
        return lines


    def preview(self):
        self.lines = [(5, 0, 0)]
        line_list=[]
        lines=self._get_lines()
        for line in lines:
            line_list.append((0,0,{
                'vendor':line.get('partner_id'),
                'amount':line.get('amount')
            }))
        self.lines=line_list
        return {
            'type': 'ir.actions.act_window',
            'res_model': "odoo_mo.top_vendor",
            'res_id': self.id,
            'view_mode': 'form,tree',
            'name': 'Top Vendors',
            'target': 'new'
        }

    def dynamic_view(self):
        lines = self._get_lines()
        for line in lines:
            line['partner_name']=self.env['res.partner'].search([('id','=',line.get('partner_id'))],limit=1).name
        return {
            'name': "Top Vendors",
            'type': 'ir.actions.client',
            'tag': 'top_vendor_view',
            'lines': lines,
        }

    def print_pdf(self):
        data={}
        lines = self._get_lines()
        data['lines']=lines
        return self.env.ref('odoo_mo_top_vendors.odoo_mo_top_vendor_action').report_action([], data=data)

    def print_excel(self):
        data = {}
        lines = self._get_lines()
        data['lines'] = lines
        return self.env.ref('odoo_mo_top_vendors.odoo_mo_top_vendor_action_xlsx').report_action([],data=data)


class Template(models.TransientModel):
    _name = 'odoo_mo.top_venodor_template'

    vendor = fields.Many2one(comodel_name="res.partner", string="Vendor", readonly=True)

    amount = fields.Float(string="Amount", readonly=True)

    wiz_id = fields.Many2one(comodel_name="odoo_mo.top_vendor")
