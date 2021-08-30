# -*- coding: utf-8 -*-

from odoo import models, fields


class PharmacyInsuranceCompanyInherit(models.Model):
    _inherit = 'res.partner'

    patients_count = fields.Integer(
        '# Patients', compute='_compute_patients_count')
    is_insurance_company = fields.Boolean(string='Insurance Company',  default=False)
    
    def _compute_patients_count(self):
        for record in self:
            count = self.env['res.partner'].sudo().search_count([('insurance_company_id', '=' ,record.id)])
        self.patients_count = count
