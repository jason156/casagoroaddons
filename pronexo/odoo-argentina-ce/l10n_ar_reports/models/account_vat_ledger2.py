##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from ast import literal_eval
import base64
import logging
import re
_logger = logging.getLogger(__name__)


class AccountVatLedger(models.Model):
    _inherit = "account.vat.ledger"

    citi_skip_invoice_tests = fields.Boolean(
        string='Skip invoice tests?',
        help='If you skip invoice tests probably you will have errors when '
        'loading the files in citi.'
    )
    citi_skip_lines = fields.Char(
        string="List of lines to skip con citi files",
        help="Enter a list of lines, for eg '1, 2, 3'. If you skip some lines "
        "you would need to enter them manually"
    )
    REGINFO_CV_ALICUOTAS = fields.Text(
        'REGINFO_CV_ALICUOTAS',
        readonly=True,
    )
    REGINFO_CV_COMPRAS_IMPORTACIONES = fields.Text(
        'REGINFO_CV_COMPRAS_IMPORTACIONES',
        readonly=True,
    )
    REGINFO_CV_CBTE = fields.Text(
        'REGINFO_CV_CBTE',
        readonly=True,
    )
    REGINFO_CV_CABECERA = fields.Text(
        'REGINFO_CV_CABECERA',
        readonly=True,
    )
    vouchers_file = fields.Binary(
        compute='_compute_files',
        readonly=True
    )
    vouchers_filename = fields.Char(
        readonly=True,
        compute='_compute_files',
    )
    aliquots_file = fields.Binary(
        compute='_compute_files',
        readonly=True
    )
    aliquots_filename = fields.Char(
        readonly=True,
        compute='_compute_files',
    )
    import_aliquots_file = fields.Binary(
        compute='_compute_files',
        readonly=True
    )
    import_aliquots_filename = fields.Char(
        readonly=True,
        compute='_compute_files',
    )
    prorate_tax_credit = fields.Boolean(
    )
    prorate_type = fields.Selection(
        [('global', 'Global'), ('by_voucher', 'By Voucher')],
    )
    tax_credit_computable_amount = fields.Float(
        'Credit Computable Amount',
    )
    sequence = fields.Integer(
        default=0,
        required=True,
        help='Se deber?? indicar si la presentaci??n es Original (00) o '
        'Rectificativa y su orden'
    )

    @api.multi
    def format_amount(self, amount, padding=15, decimals=2, invoice=False):
        # get amounts on correct sign despite conifiguration on taxes and tax
        # codes
        # TODO
        # remove this and perhups invoice argument (we always send invoice)
        # for invoice refund we dont change sign (we do this before)
        # if invoice:
        #     amount = abs(amount)
        #     if invoice.type in ['in_refund', 'out_refund']:
        #         amount = -1.0 * amount
        # Al final volvimos a agregar esto, lo necesitabamos por ej si se pasa
        # base negativa de no gravado

        if amount < 0:
            template = "-{:0>%dd}" % (padding - 1)
        else:
            template = "{:0>%dd}" % (padding)
        return template.format(
            int(round(abs(amount) * 10**decimals, decimals)))

    @api.multi
    @api.depends(
        'REGINFO_CV_CBTE',
        'REGINFO_CV_ALICUOTAS',
        'type',
        # 'period_id.name'
    )
    def _compute_files(self):
        self.ensure_one()
        # segun vimos aca la afip espera "ISO-8859-1" en vez de utf-8
        # http://www.planillasutiles.com.ar/2015/08/
        # como-descargar-los-archivos-de.html
        if self.REGINFO_CV_ALICUOTAS:
            self.aliquots_filename = _('Alicuots_%s_%s.txt') % (
                self.type,
                self.date_to,
                # self.period_id.name
            )
            self.aliquots_file = base64.encodestring(
                self.REGINFO_CV_ALICUOTAS.encode('ISO-8859-1'))
        if self.REGINFO_CV_COMPRAS_IMPORTACIONES:
            self.import_aliquots_filename = _('Import_Alicuots_%s_%s.txt') % (
                self.type,
                self.date_to,
                # self.period_id.name
            )
            self.import_aliquots_file = base64.encodestring(
                self.REGINFO_CV_COMPRAS_IMPORTACIONES.encode('ISO-8859-1'))
        if self.REGINFO_CV_CBTE:
            self.vouchers_filename = _('Vouchers_%s_%s.txt') % (
                self.type,
                self.date_to,
                # self.period_id.name
            )
            self.vouchers_file = base64.encodestring(
                self.REGINFO_CV_CBTE.encode('ISO-8859-1'))

    @api.multi
    def compute_citi_data(self):
        alicuotas = self.get_REGINFO_CV_ALICUOTAS()
        # sacamos todas las lineas y las juntamos
        lines = []
        for k, v in alicuotas.items():
            lines += v
        self.REGINFO_CV_ALICUOTAS = '\r\n'.join(lines)

        impo_alicuotas = {}
        if self.type == 'purchase':
            impo_alicuotas = self.get_REGINFO_CV_ALICUOTAS(impo=True)
            # sacamos todas las lineas y las juntamos
            lines = []
            for k, v in impo_alicuotas.items():
                lines += v
            self.REGINFO_CV_COMPRAS_IMPORTACIONES = '\r\n'.join(lines)
        alicuotas.update(impo_alicuotas)
        self.get_REGINFO_CV_CBTE(alicuotas)

    @api.model
    def get_partner_document_code(self, partner):
        # se exige cuit para todo menos consumidor final.
        # TODO si es mayor a 1000 habria que validar reportar
        # DNI, LE, LC, CI o pasaporte
        if partner.l10n_ar_afip_responsibility_type_id.code == '5':
            return "{:0>2d}".format(partner.l10n_latam_identification_type_id.l10n_ar_afip_code)
        return '80'

    @api.model
    def get_partner_document_number(self, partner):
        # se exige cuit para todo menos consumidor final.
        # TODO si es mayor a 1000 habria que validar reportar
        # DNI, LE, LC, CI o pasaporte
        if partner.l10n_ar_afip_responsibility_type_id.code == '5':
            number = partner.vat or ''
            # por las dudas limpiamos letras
            number = re.sub("[^0-9]", "", number)
        else:
            number = partner.cuit_required()
        return number.rjust(20, '0')

    @api.model
    def get_point_of_sale(self, invoice):
        return "{:0>5d}".format(invoice.point_of_sale_number)

    def action_see_skiped_invoices(self):
        invoices = self.get_citi_invoices(return_skiped=True)
        raise ValidationError(_('Facturas salteadas:\n%s') % ', '.join(invoices.mapped('display_name')))

    @api.constrains('citi_skip_lines')
    def _check_citi_skip_lines(self):
        for rec in self.filtered('citi_skip_lines'):
            try:
                res = literal_eval(rec.citi_skip_lines)
                if not isinstance(res, int):
                    assert isinstance(res, tuple)
            except Exception as e:
                raise ValidationError(_(
                    'Bad format for Skip Lines. You need to enter a list of '
                    'numbers like "1, 2, 3". This is the error we get: %s') % (
                        repr(e)))

    @api.multi
    def get_citi_invoices(self, return_skiped=False):
        self.ensure_one()
        invoices = self.env['account.move'].search([
            ('document_type_id.export_to_citi', '=', True),
            ('id', 'in', self.invoice_ids.ids)], order='date_invoice asc')
        if self.citi_skip_lines:
            skip_lines = literal_eval(self.citi_skip_lines)
            if isinstance(skip_lines, int):
                skip_lines = [skip_lines]
            to_skip = invoices.browse()
            for line in skip_lines:
                to_skip += invoices[line - 1]
            if return_skiped:
                return to_skip
            invoices -= to_skip
        return invoices

    @api.multi
    def get_REGINFO_CV_CBTE(self, alicuotas):
        self.ensure_one()
        res = []
        invoices = self.get_citi_invoices()
        if not self.citi_skip_invoice_tests:
            invoices.check_argentinian_invoice_taxes()
        if self.type == 'purchase':
            partners = invoices.mapped('commercial_partner_id').filtered(
                lambda r: r.l10n_latam_identification_type_id.l10n_ar_afip_code in (
                    False, 99) or not r.vat)
            if partners:
                raise ValidationError(_(
                    "On purchase citi, partner document type is mandatory "
                    "and it must be different from 99. "
                    "Partners: \r\n\r\n"
                    "%s") % '\r\n'.join(
                        ['[%i] %s' % (p.id, p.display_name)
                            for p in partners]))

        for inv in invoices:
            # si no existe la factura en alicuotas es porque no tienen ninguna
            cant_alicuotas = len(alicuotas.get(inv))

            currency_rate = inv.currency_rate
            currency_code = inv.currency_id.l10n_ar_afip_code

            row = [
                # Campo 1: Fecha de comprobante
                fields.Date.from_string(inv.date_invoice).strftime('%Y%m%d'),

                # Campo 2: Tipo de Comprobante.
                "{:0>3d}".format(int(inv.document_type_id.code)),

                # Campo 3: Punto de Venta
                self.get_point_of_sale(inv),

                # Campo 4: N??mero de Comprobante
                # TODO agregar estos casos de uso
                # Si se trata de un comprobante de varias hojas, se deber??
                # informar el n??mero de documento de la primera hoja, teniendo
                # en cuenta lo normado en el  art??culo 23, inciso a), punto
                # 6., de la Resoluci??n General N?? 1.415, sus modificatorias y
                # complementarias.
                # En el supuesto de registrar de manera agrupada por totales
                # diarios, se deber?? consignar el primer n??mero de comprobante
                # del rango a considerar.
                "{:0>20d}".format(inv.invoice_number)
            ]

            if self.type == 'sale':
                # Campo 5: N??mero de Comprobante Hasta.
                # TODO agregar esto En el resto de los casos se consignar?? el
                # dato registrado en el campo 4
                row.append("{:0>20d}".format(inv.invoice_number))
            else:
                # Campo 5: Despacho de importaci??n
                if inv.document_type_id.code == '66':
                    row.append(
                        (inv.l10n_latam_document_number or inv.name or '').rjust(
                            16, '0'))
                else:
                    row.append(''.rjust(16, ' '))

            row += [
                # Campo 6: C??digo de documento del comprador.
                self.get_partner_document_code(inv.commercial_partner_id),

                # Campo 7: N??mero de Identificaci??n del comprador
                self.get_partner_document_number(inv.commercial_partner_id),

                # Campo 8: Apellido y Nombre del comprador.
                inv.commercial_partner_id.name.ljust(30, ' ')[:30],
                # inv.commercial_partner_id.name.encode(
                #     'ascii', 'replace').ljust(30, ' ')[:30],

                # Campo 9: Importe Total de la Operaci??n.
                self.format_amount(inv.cc_amount_total, invoice=inv),

                # Campo 10: Importe total de conceptos que no integran el
                # precio neto gravado
                self.format_amount(
                    inv.cc_vat_untaxed_base_amount, invoice=inv),
            ]

            if self.type == 'sale':
                row += [
                    # Campo??11:??Percepci??n a no categorizados
                    self.format_amount(
                        sum(inv.tax_line_ids.filtered(lambda r: (
                            r.tax_id.tax_group_id.type == 'perception' and
                            r.tax_id.tax_group_id.tax == 'vat' and
                            r.tax_id.tax_group_id.application \
                            == 'national_taxes')
                        ).mapped('cc_amount')), invoice=inv),

                    # Campo 12: Importe de operaciones exentas
                    self.format_amount(
                        inv.cc_vat_exempt_base_amount, invoice=inv),
                ]
            else:
                row += [
                    # Campo 11: Importe de operaciones exentas
                    self.format_amount(
                        inv.cc_vat_exempt_base_amount, invoice=inv),

                    # Campo 12: Importe de percepciones o pagos a cuenta del
                    # Impuesto al Valor Agregado
                    self.format_amount(
                        sum(inv.tax_line_ids.filtered(lambda r: (
                            r.tax_id.tax_group_id.type == 'perception' and
                            r.tax_id.tax_group_id.tax == 'vat' and
                            r.tax_id.tax_group_id.application \
                            == 'national_taxes')
                        ).mapped(
                            'cc_amount')), invoice=inv),
                ]

            row += [
                # Campo??13:??Importe de percepciones o pagos a cuenta de
                # impuestos nacionales
                self.format_amount(
                    sum(inv.tax_line_ids.filtered(lambda r: (
                        r.tax_id.tax_group_id.type == 'perception' and
                        r.tax_id.tax_group_id.tax != 'vat' and
                        r.tax_id.tax_group_id.application == 'national_taxes')
                    ).mapped('cc_amount')), invoice=inv),

                # Campo 14: Importe de percepciones de ingresos brutos
                self.format_amount(
                    sum(inv.tax_line_ids.filtered(lambda r: (
                        r.tax_id.tax_group_id.type == 'perception' and
                        r.tax_id.tax_group_id.application \
                        == 'provincial_taxes')
                    ).mapped('cc_amount')), invoice=inv),

                # Campo 15: Importe de percepciones de impuestos municipales
                self.format_amount(
                    sum(inv.tax_line_ids.filtered(lambda r: (
                        r.tax_id.tax_group_id.type == 'perception' and
                        r.tax_id.tax_group_id.application == 'municipal_taxes')
                    ).mapped('cc_amount')), invoice=inv),

                # Campo 16: Importe de impuestos internos
                self.format_amount(
                    sum(inv.tax_line_ids.filtered(
                        lambda r: r.tax_id.tax_group_id.application \
                        == 'internal_taxes'
                    ).mapped('cc_amount')), invoice=inv),

                # Campo 17: C??digo de Moneda
                str(currency_code),

                # Campo 18: Tipo de Cambio
                # nueva modalidad de currency_rate
                self.format_amount(currency_rate, padding=10, decimals=6),

                # Campo 19: Cantidad de al??cuotas de IVA
                str(cant_alicuotas),

                # Campo 20: C??digo de operaci??n.
                # WARNING. segun la plantilla es 0 si no es ninguna
                # TODO ver que no se informe un codigo si no correpsonde,
                # tal vez da error
                # TODO ADIVINAR E IMPLEMENTAR, VA A DAR ERROR
                inv.fiscal_position_id.l10n_ar_afip_code or '0',
            ]

            if self.type == 'sale':
                row += [
                    # Campo 21: Otros Tributos
                    self.format_amount(
                        sum(inv.tax_line_ids.filtered(
                            lambda r: r.tax_id.tax_group_id.application \
                            == 'others'
                        ).mapped('cc_amount')), invoice=inv),

                    # Campo 22: vencimiento comprobante (no figura en
                    # instructivo pero si en aplicativo) para tique y factura
                    # de exportacion no se informa, tmb para algunos otros
                    # pero que tampoco tenemos implementados
                    (inv.document_type_id.code in [
                        '19', '20', '21', '16', '55', '81', '82', '83',
                        '110', '111', '112', '113', '114', '115', '116',
                        '117', '118', '119', '120', '201', '202', '203',
                        '206', '207', '208', '211', '212', '213'] and
                        '00000000' or
                        fields.Date.from_string(
                            inv.date_due or inv.date_invoice).strftime(
                            '%Y%m%d')),
                ]
            else:
                # Campo 21: Cr??dito Fiscal Computable
                if self.prorate_tax_credit:
                    if self.prorate_type == 'global':
                        row.append(self.format_amount(0, invoice=inv))
                    else:
                        # row.append(self.format_amount(0))
                        # por ahora no implementado pero seria lo mismo que
                        # sacar si prorrateo y que el cliente entre en el citi
                        # en cada comprobante y complete cuando es en
                        # credito fiscal computable
                        raise ValidationError(_(
                            'Para utilizar el prorrateo por comprobante:\n'
                            '1) Exporte los archivos sin la opci??n "Proratear '
                            'Cr??dito de Impuestos"\n2) Importe los mismos '
                            'en el aplicativo\n3) En el aplicativo de afip, '
                            'comprobante por comprobante, indique el valor '
                            'correspondiente en el campo "Cr??dito Fiscal '
                            'Computable"'))
                else:
                    row.append(self.format_amount(
                        inv.cc_vat_amount, invoice=inv))

                row += [
                    # Campo 22: Otros Tributos
                    self.format_amount(
                        sum(inv.tax_line_ids.filtered(lambda r: (
                            r.tax_id.tax_group_id.application \
                            == 'others')).mapped(
                            'cc_amount')), invoice=inv),

                    # TODO implementar estos 3
                    # Campo 23: CUIT Emisor / Corredor
                    # Se informar?? s??lo si en el campo "Tipo de Comprobante" se
                    # consigna '033', '058', '059', '060' ?? '063'. Si para
                    # ??stos comprobantes no interviene un tercero en la
                    # operaci??n, se consignar?? la C.U.I.T. del informante. Para
                    # el resto de los comprobantes se completar?? con ceros
                    self.format_amount(0, padding=11, invoice=inv),

                    # Campo 24: Denominaci??n Emisor / Corredor
                    ''.ljust(30, ' ')[:30],

                    # Campo 25: IVA Comisi??n
                    # Si el campo 23 es distinto de cero se consignar?? el
                    # importe del I.V.A. de la comisi??n
                    self.format_amount(0, invoice=inv),
                ]
            res.append(''.join(row))
        self.REGINFO_CV_CBTE = '\r\n'.join(res)

    @api.multi
    def get_tax_row(self, invoice, base, code, tax_amount, impo=False):
        self.ensure_one()
        inv = invoice
        if self.type == 'sale':
            row = [
                # Campo 1: Tipo de Comprobante
                "{:0>3d}".format(int(inv.document_type_id.code)),

                # Campo 2: Punto de Venta
                self.get_point_of_sale(inv),

                # Campo 3: N??mero de Comprobante
                "{:0>20d}".format(inv.invoice_number),

                # Campo 4: Importe Neto Gravado
                self.format_amount(base, invoice=inv),

                # Campo 5: Al??cuota de IVA.
                str(code).rjust(4, '0'),

                # Campo 6: Impuesto Liquidado.
                self.format_amount(tax_amount, invoice=inv),
            ]
        elif impo:
            row = [
                # Campo 1: Despacho de importaci??n.
                (inv.l10n_latam_document_number or inv.name or '').rjust(16, '0'),

                # Campo 2: Importe Neto Gravado
                self.format_amount(base, invoice=inv),

                # Campo 3: Al??cuota de IVA
                str(code).rjust(4, '0'),

                # Campo 4: Impuesto Liquidado.
                self.format_amount(tax_amount, invoice=inv),
            ]
        else:
            row = [
                # Campo 1: Tipo de Comprobante
                "{:0>3d}".format(int(inv.document_type_id.code)),

                # Campo 2: Punto de Venta
                self.get_point_of_sale(inv),

                # Campo 3: N??mero de Comprobante
                "{:0>20d}".format(inv.invoice_number),

                # Campo 4: C??digo de documento del vendedor
                self.get_partner_document_code(
                    inv.commercial_partner_id),

                # Campo 5: N??mero de identificaci??n del vendedor
                self.get_partner_document_number(
                    inv.commercial_partner_id),

                # Campo 6: Importe Neto Gravado
                self.format_amount(base, invoice=inv),

                # Campo 7: Al??cuota de IVA.
                str(code).rjust(4, '0'),

                # Campo 8: Impuesto Liquidado.
                self.format_amount(tax_amount, invoice=inv),
            ]
        return row

    @api.multi
    def get_REGINFO_CV_ALICUOTAS(self, impo=False):
        """
        Devolvemos un dict para calcular la cantidad de alicuotas cuando
        hacemos los comprobantes
        """
        self.ensure_one()
        res = {}
        # only vat taxes with codes 3, 4, 5, 6, 8, 9
        # segun: http://contadoresenred.com/regimen-de-informacion-de-
        # compras-y-ventas-rg-3685-como-cargar-la-informacion/
        # empezamos a contar los codigos 1 (no gravado) y 2 (exento)
        # si no hay alicuotas, sumamos una de esta con 0, 0, 0 en detalle
        # usamos mapped por si hay afip codes duplicados (ej. manual y
        # auto)
        if impo:
            invoices = self.get_citi_invoices().filtered(
                lambda r: r.document_type_id.code == '66')
        else:
            invoices = self.get_citi_invoices().filtered(
                lambda r: r.document_type_id.code != '66')
        for inv in invoices:
            lines = []
            is_zero = inv.currency_id.is_zero
            # reportamos como linea de iva si:
            # * el impuesto es iva cero
            # * el impuesto es iva 21, 27 etc pero tiene impuesto liquidado,
            # si no tiene impuesto liquidado (is_zero), entonces se inventa
            # una linea
            vat_taxes = inv.vat_tax_ids.filtered(
                lambda r: r.tax_id.tax_group_id.l10n_ar_afip_code == 3 or (
                    r.tax_id.tax_group_id.l10n_ar_afip_code in [
                        4, 5, 6, 8, 9] and not is_zero(r.amount)))

            if not vat_taxes and inv.vat_tax_ids.filtered(
                    lambda r: r.tax_id.tax_group_id.l10n_ar_afip_code):
                lines.append(''.join(self.get_tax_row(
                    inv, 0.0, 3, 0.0, impo=impo)))

            # we group by afip_code
            for afip_code in vat_taxes.mapped('tax_id.tax_group_id.l10n_ar_afip_code'):
                taxes = vat_taxes.filtered(
                    lambda x: x.tax_id.tax_group_id.l10n_ar_afip_code == afip_code)
                imp_neto = sum(taxes.mapped('cc_base'))
                imp_liquidado = sum(taxes.mapped('cc_amount'))
                lines.append(''.join(self.get_tax_row(
                    inv,
                    imp_neto,
                    afip_code,
                    imp_liquidado,
                    impo=impo,
                )))
            res[inv] = lines
        return res
