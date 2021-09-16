# -*- coding: utf-8 -*-
from odoo import api, models, fields, _


class SaleOrderLineInherit(models.Model):
    _inherit = 'sale.order.line'

    is_warning = fields.Boolean(string='is_warning', default=False)
    clinical_history_id = fields.Many2one(
        'pharmacy.clinical.history', string="Clinical History")

    @api.onchange('product_id')
    def show_warning(self):
        if self.product_id.exists():
            clinical_history_ids = self.env['pharmacy.clinical.history'].sudo(
            ).search([('name', '=', self.order_id.partner_id.id)])
            print(clinical_history_ids)
            for record in clinical_history_ids:
                self.check_reaction(record)

    def check_reaction(self, clinical_history_id):
        disease_ids = clinical_history_id.disease_ids
        for _ in disease_ids.filtered(
                lambda x: self.product_id.id in x.reaction_medicine_ids.ids):
            self.is_warning = True
            self.clinical_history_id =clinical_history_id
            return self.is_warning
        return False

    def _prepare_invoice_line_with_copayment(
        self, copayment=None, is_customer_invoice='False', **optional_values):
        res = self._prepare_invoice_line()
        if(is_customer_invoice):
            res['price_unit'] = self.price_unit * copayment/100
        else:
            res['price_unit'] = self.price_unit * (100-copayment)/100
            res['quantity'] = self.product_uom_qty
        return res

    def _get_to_invoice_qty(self):
        super(SaleOrderLineInherit, self)._get_to_invoice_qty()
        for line in self:
            if line.qty_to_invoice < 0:
                line.qty_to_invoice = 0

    def _get_invoice_qty(self):
        super(SaleOrderLineInherit, self)._get_invoice_qty()
        for line in self:
            if line.qty_invoiced > line.product_uom_qty:
                line.qty_invoiced = line.product_uom_qty

    def action_clinical_history(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Medicine might cause reaction '
            'considering this Clinical History!'),
            'view_mode': 'form',
            'res_model': 'pharmacy.clinical.history',
            'target': 'new',
            'res_id': self.clinical_history_id.id,
        }
