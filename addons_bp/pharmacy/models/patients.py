# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from lxml import etree

class PharmacyPatientInherit(models.Model):
    _inherit = 'res.partner'

    insurance_company_id = fields.Many2one(
        'res.partner', string='Insurance Company Name')
    insurance_no = fields.Char(string='Insurance No.')
    clinical_history_ids = fields.One2many(
        'pharmacy.clinical.history', 'name', string="Clinical History")
    copayment = fields.Float(string = 'Co-payment', default=0, help="Indicates the percentage of amount paid by the customer")

    @api.constrains('copayment')
    def check_copayment(self):
        for rec in self:
            if not (0.0<= rec.copayment <= 100.0):
                raise ValidationError(_("Co-payment must be between 0 and 100"))

    def print_report(self):
        return self.env.ref('pharmacy.report_patient_clinical_history').report_action(self)
