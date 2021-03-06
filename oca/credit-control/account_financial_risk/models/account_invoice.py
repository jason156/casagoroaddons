# Copyright 2016-2018 Tecnativa - Carlos Dauden
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, models


class AccountMove(models.Model):
    _inherit = "account.move"

    def risk_exception_msg(self):
        self.ensure_one()
        partner = self.partner_id.commercial_partner_id
        exception_msg = ""
        if partner.risk_exception:
            exception_msg = _("Financial risk exceeded.\n")
        elif partner.risk_invoice_open_limit and (
            (partner.risk_invoice_open + self.amount_total_signed)
            > partner.risk_invoice_open_limit
        ):
            exception_msg = _("This invoice exceeds the open invoices risk.\n")
        # If risk_invoice_draft_include this invoice included in risk_total
        elif not partner.risk_invoice_draft_include and (
            partner.risk_invoice_open_include
            and (partner.risk_total + self.amount_total_signed) > partner.credit_limit
        ):
            exception_msg = _("This invoice exceeds the financial risk.\n")
        return exception_msg

    def post(self):
        if (
            self.env.context.get("bypass_risk", False)
            or self.company_id.allow_overrisk_invoice_validation
        ):
            return super().post()
        for invoice in self.filtered(lambda x: x.type == "out_invoice"):
            exception_msg = invoice.risk_exception_msg()
            if exception_msg:
                return (
                    self.env["partner.risk.exceeded.wiz"]
                    .create(
                        {
                            "exception_msg": exception_msg,
                            "partner_id": invoice.partner_id.commercial_partner_id.id,
                            "origin_reference": "{},{}".format(
                                "account.move", invoice.id
                            ),
                            "continue_method": "post",
                        }
                    )
                    .action_show()
                )
        return super().post()
