# -*- coding: utf-8 -*-

from odoo import models, fields


class PharmacyPatientInherit(models.Model):
    _inherit = 'res.partner'

    insurance_no = fields.Char(string='Insurance No.')
    clinical_history_ids = fields.One2many(
        'pharmacy.clinical.history', 'name', string="Clinical History")
