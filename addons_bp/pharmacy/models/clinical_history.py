# -*- coding: utf-8 -*-

from odoo import models, fields
from datetime import datetime


class ClinicalHistory(models.Model):
    _name = 'pharmacy.clinical.history'
    _description = 'Clinical history of patients'

    name = fields.Many2one(
        'res.partner', string='Patient', required=True)
    date = fields.Date(default=datetime.today())
    disease_ids = fields.Many2many(
        'pharmacy.disease.details', string="Disease", required=True)
    medicine_ids = fields.Many2many(
        'product.product', string="Medicines")
