# -*- coding: utf-8 -*-

from odoo import models, fields


class ClinicalHistory(models.Model):
    _name = 'pharmacy.clinical.history'
    _description = 'Clinical history of patients'

    name = fields.Many2one(
        'res.partner', string='Patient')
    date = fields.Date(string='Date')
    diseases = fields.Many2many('pharmacy.disease.details', string="Disease")
