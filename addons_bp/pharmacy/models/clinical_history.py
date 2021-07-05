# -*- coding: utf-8 -*-

from odoo import models, fields


class ClinicalHistory(models.Model):
    _name = 'pharmacy.clinical.history'
    _description = 'Clinical history of patients'

    patient_name = fields.Many2one(
        'pharmacy.patient', string='Patient')
    disease = fields.Char(string="Disease")
    reaction_medicine = fields.Many2many(
        'product.template', string='Reaction to')
