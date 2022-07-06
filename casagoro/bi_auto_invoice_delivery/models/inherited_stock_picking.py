# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.tools.misc import formatLang, format_date, get_lang
from odoo.tools import float_is_zero, float_compare


class Picking(models.Model):
    _inherit = "stock.picking"

    @api.depends('state')
    def _get_invoiced(self):
        for order in self:
            invoice_ids = self.env['account.move'].search([('picking_id','=',order.id)])
            order.invoice_count = len(invoice_ids)
    invoice_count = fields.Integer(string='# of Invoices', compute='_get_invoiced')
    
    def button_view_invoice(self):
        mod_obj = self.env['ir.model.data']
        act_obj = self.env['ir.actions.act_window']
        work_order_id = self.env['account.move'].search([('picking_id', '=', self.id)])
        inv_ids = []
        action = self.env.ref('account.action_move_out_invoice_type').read()[0]
        context = {
            'default_type': work_order_id[0].type,
        }
        action['domain'] = [('id', 'in', work_order_id.ids)]
        action['context'] = context
        return action

    
    def action_done(self):

        action = super(Picking, self).action_done()
        res_config = self.env['res.config.settings'].sudo().search([],order="id desc", limit=1)
        if self.state == 'done':    

            if self.picking_type_id.code == 'outgoing':
                if self.origin:
                    pass
                else:
                    self.update({'origin': self._context.get('default_origin')})

                sale_order  =  self.env['sale.order'].search([('name', '=',self.origin)])

                if sale_order:
                    invoice = sale_order._create_invoices()
                    invoice.write({
                        'picking_id':self.id
                    })
                    if res_config.auto_validate_invoice == True :
                        invoice.action_post()    
                    if res_config.auto_validate_invoice == True and res_config.auto_send_mail_invoice == True:
                        template = self.env.ref('account.email_template_edi_invoice', False)            
                        send = invoice.with_context(force_send=True,model_description='Invoice').message_post_with_template(int(template),email_layout_xmlid="mail.mail_notification_paynow")
        return action