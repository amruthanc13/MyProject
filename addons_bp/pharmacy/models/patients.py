# -*- coding: utf-8 -*-

from odoo import models, fields


class PharmacyPatientInherit(models.Model):
    _inherit = 'res.partner'

    insurance_no = fields.Char(string='Insurance No.')
    clinical_history = fields.One2many(
        'pharmacy.clinical.history', 'name', string="Clinical History")


class MedicineProductInherit(models.Model):
    _inherit = 'product.product'

    medicine_code = fields.Char(string='International drug code')
