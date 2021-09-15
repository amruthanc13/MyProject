# -*- coding: utf-8 -*-
import base64
from odoo import api, models, fields, _
from odoo.exceptions import AccessError, ValidationError
from itertools import groupby


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    disease_ids = fields.Many2many(
        'pharmacy.disease.details', string='Diseases')
    prescription = fields.Binary(string="Prescription")
    prescription_name = fields.Char(string="File Name")
    doctor_name = fields.Many2one(
        'res.partner', string='Doctor', domain="[('is_company', '!=', True)]")

    def check_prescription(self):
        for line in self.order_line:
            if (line.product_id.prescription_required) and not self.prescription:
                raise ValidationError(
                    _("%s cannot be solved without prescription.", line.name))

    def action_confirm(self):
        self.check_prescription()
        res = super(SaleOrderInherit, self).action_confirm()
        if self.state == 'sale' and self.disease_ids.exists():
            vals = {'name': self.partner_id.id,
                    'date': self.date_order,
                    'disease_ids': [(6, 0, self.disease_ids.ids)],
                    'medicine_ids': [(6, 0, self.order_line.product_id.ids)]}
            self.env['pharmacy.clinical.history'].create(vals)
        res = self.confirm_report()
        return res

    def confirm_report(self):
        confirmation_report = self.env['ir.config_parameter'].sudo(
        ).get_param('pharmacy.confirmation_report')
        if confirmation_report:
            dynamic_report_id = self.env['ir.config_parameter'].sudo(
            ).get_param('pharmacy.dynamic_report_template_id')
            template_id = self.env['dynamic.report.template'].search(
                [('id', '=', dynamic_report_id)])
            pdfs = template_id.generate_pdf(self.ids)
            data = base64.b64encode(pdfs[self.id])
            base_url = self.env['ir.config_parameter'].get_param(
                'web.base.url')
            attachment_id = self.env['ir.attachment'].create({
                'name': f"Confirm Report {self.name}.pdf",
                'res_id': self.id,
                'res_model': self._context.get('active_model'),
                'datas': data,
                'description': self.id,
                'type': 'binary',
            })
            email_template_id = self.env.ref(
                'pharmacy.confirm_order_email_template').id
            email_template = self.env['mail.template'].browse(
                email_template_id)
            email_template.attachment_ids = [(6, 0, [attachment_id.id])]
            email_template.send_mail(self.id, force_send=True)
        return True

    def _prepare_invoice(self):
        invoice_vals = super(SaleOrderInherit, self)._prepare_invoice()
        partner = self.env['res.partner'].browse(
            invoice_vals.get('partner_id'))
        if partner.insurance_company_id.exists() and (self.prescription):
            if(partner.copayment == 0):
                invoice_vals['partner_id'] = partner.insurance_company_id.address_get(
                    ['contact'])['contact']
            elif(partner.copayment == 100):
                invoice_vals['partner_id'] = self.partner_invoice_id.id
        return invoice_vals

    def _create_invoices_copayment(
            self, grouped=False, final=False, date=None, copayment=None):
        if not self.env['account.move'].check_access_rights('create', False):
            try:
                self.check_access_rights('write')
                self.check_access_rule('write')
            except AccessError:
                return self.env['account.move']

        invoice_vals_list = []
        # Incremental sequencing to keep the lines order on the invoice.
        invoice_item_sequence = 0
        is_customer_invoice = True
        count = 0
        invoiceable_lines = self._get_invoiceable_lines()
        while count <= 1:
            self = self.with_company(self.company_id)
            current_section_vals = None
            down_payments = self.env['sale.order.line']

            invoice_vals = self._prepare_invoice_with_copayment(
                invoice_type=is_customer_invoice)

            if not any(not line.display_type for line in invoiceable_lines):
                raise self._nothing_to_invoice_error()

            invoice_line_vals = []
            down_payment_section_added = False

            for line in invoiceable_lines:
                if not down_payment_section_added and line.is_downpayment:
                    # Create a dedicated section for the down payments
                    # (put at the end of the invoiceable_lines)
                    invoice_line_vals.append(
                        (0, 0, self._prepare_down_payment_section_line(
                            sequence=invoice_item_sequence,
                        )),
                    )
                    dp_section = True
                    invoice_item_sequence += 1
                invoice_line_vals.append(
                    (0, 0, line._prepare_invoice_line_with_copayment(copayment,
                                                                     is_customer_invoice,
                                                                     sequence=invoice_item_sequence,
                                                                     )),
                )
                invoice_item_sequence += 1

            invoice_vals['invoice_line_ids'] += invoice_line_vals
            invoice_vals_list.append(invoice_vals)

            if not invoice_vals_list:
                raise self._nothing_to_invoice_error()

            if not grouped:
                new_invoice_vals_list = []
                invoice_grouping_keys = self._get_invoice_grouping_keys()
                for grouping_keys, invoices in groupby(invoice_vals_list, key=lambda x: [x.get(
                    grouping_key) for grouping_key in invoice_grouping_keys]):
                    origins = set()
                    payment_refs = set()
                    refs = set()
                    ref_invoice_vals = None

                    for invoice_vals in invoices:

                        if not ref_invoice_vals:
                            ref_invoice_vals = invoice_vals
                        else:
                            ref_invoice_vals['invoice_line_ids'] += invoice_vals['invoice_line_ids']
                        origins.add(invoice_vals['invoice_origin'])
                        payment_refs.add(invoice_vals['payment_reference'])
                        refs.add(invoice_vals['ref'])
                    ref_invoice_vals.update({
                        'ref': ', '.join(refs)[:2000],
                        'invoice_origin': ', '.join(origins),
                        'payment_reference': len(payment_refs) == 1 and payment_refs.pop() or False,
                    })
                new_invoice_vals_list.append(ref_invoice_vals)
            invoice_vals_list = new_invoice_vals_list

            if len(invoice_vals_list) < len(self):
                SaleOrderLine = self.env['sale.order.line']

                for invoice in invoice_vals_list:
                    sequence = 1
                    for line in invoice['invoice_line_ids']:
                        line[2]['sequence'] = SaleOrderLine._get_invoice_line_sequence(
                            new=sequence, old=line[2]['sequence'])
                        sequence += 1

            moves = self.env['account.move'].sudo().with_context(
                default_move_type='out_invoice').create(invoice_vals_list)

            if final:
                moves.sudo().filtered(lambda m: m.amount_total <
                                      0).action_switch_invoice_into_refund_credit_note()
            for move in moves:
                move.message_post_with_view('mail.message_origin_link',
                                            values={'self': move, 'origin': move.line_ids.mapped(
                                                'sale_line_ids.order_id')},
                                            subtype_id=self.env.ref(
                                                'mail.mt_note').id
                                            )

            is_customer_invoice = False
            count += 1

        return moves

    def _prepare_invoice_with_copayment(self, invoice_type=False):
        invoice_vals = self._prepare_invoice()
        partner = self.env['res.partner'].browse(
            invoice_vals.get('partner_id'))
        if invoice_type:
            invoice_vals['partner_id'] = self.partner_invoice_id.id
        else:
            invoice_vals['partner_id'] = partner.insurance_company_id.address_get(['contact'])[
                'contact']
        return invoice_vals

    def _create_invoices(self, grouped=False, final=False, date=None):
        for order in self:
            if order.partner_id.insurance_company_id.exists() and (
                0.0 < order.partner_id.copayment < 100.0) and (order.prescription):
                moves = order._create_invoices_copayment(
                    copayment=order.partner_id.copayment)
            else:
                moves = super(SaleOrderInherit, order)._create_invoices()
        return moves
