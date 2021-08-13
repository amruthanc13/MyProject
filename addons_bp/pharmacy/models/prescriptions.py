# -*- coding: utf-8 -*-
from odoo import api, models, fields


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    disease_ids = fields.Many2many(
        'pharmacy.disease.details', string='Diseases')

    def action_confirm(self):
        super(SaleOrderInherit, self).action_confirm()
        if self.state == 'sale' and self.disease_ids.exists():
            vals = {'name': self.partner_id.id,
                    'date': self.date_order,
                    'disease_ids': [(6, 0, self.disease_ids.ids)],
                    'medicine_ids': [(6,0, self.order_line.product_id.ids)]}
            self.env['pharmacy.clinical.history'].create(vals)
        return True

    # def _prepare_invoice(self):
    #     invoice_vals = super(SaleOrderInherit, self)._prepare_invoice()
    #     partner = self.env['res.partner'].browse(
    #         invoice_vals.get('partner_id'))
    #     if partner.insurance_company_id.exists():
    #         invoice_vals['partner_id'] = partner.insurance_company_id.address_get(['contact'])[
    #             'contact']
    #     return invoice_vals

    def _prepare_invoice(self):
        invoice_vals = super(SaleOrderInherit, self)._prepare_invoice()
        partner = self.env['res.partner'].browse(
            invoice_vals.get('partner_id'))
        if partner.insurance_company_id.exists():
            if(partner.copayment == 0):
                invoice_vals['partner_id'] = partner.insurance_company_id.address_get(['contact'])[
                'contact']
            elif(partner.copayment == 100):
                invoice_vals['partner_id'] = self.partner_invoice_id.id
        return invoice_vals

    # def _create_invoices(self, grouped=False, final=False, date=None):
    #     moves = super(SaleOrderInherit,self)._create_invoices()
    #     for order in self:
    #         partner= self.env['res.partner'].browse(order.partner_id.id)
    #         if partner.insurance_company_id.exists() and (0.0 < partner.copayment < 100.0):
    #             print(partner.copayment)
    #     return moves
