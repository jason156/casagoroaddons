# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    def _get_name_invoice_report(self, report_xml_id):
        self.ensure_one()
        if not self.l10n_latam_use_documents and self.company_id.country_id.code == 'AR':
            custom_report = {
                'account.report_invoice_document_with_payments': 'recibox.report_invoice_document_with_payments',
                'account.report_invoice_document': 'recibox.report_invoice_document',
            }
            return custom_report.get(report_xml_id) or report_xml_id
        return super()._get_name_invoice_report(report_xml_id)


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    recibox_price_unit = fields.Monetary(
        compute='compute_recibox_prices_and_taxes')
    recibox_price_subtotal = fields.Monetary(
        compute='compute_recibox_prices_and_taxes')
    recibox_price_net = fields.Monetary(
        compute='compute_recibox_prices_and_taxes')

    @api.depends('price_unit', 'price_subtotal')
    def compute_recibox_prices_and_taxes(self):
        for line in self:
            invoice = line.move_id
            included_taxes = line.tax_ids
            not_included_taxes = line.tax_ids - included_taxes
            recibox_price_unit = included_taxes.compute_all(
                line.price_unit, invoice.currency_id, 1.0, line.product_id, invoice.partner_id)['total_included']
            recibox_price_net = recibox_price_unit * \
                (1 - (line.discount or 0.0) / 100.0)
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            recibox_price_subtotal = included_taxes.compute_all(
                price, invoice.currency_id, line.quantity, line.product_id,
                invoice.partner_id)['total_included']

            line.recibox_price_subtotal = recibox_price_subtotal
            line.recibox_price_unit = recibox_price_unit
            line.recibox_price_net = recibox_price_net
            line.recibox_tax_ids = not_included_taxes
