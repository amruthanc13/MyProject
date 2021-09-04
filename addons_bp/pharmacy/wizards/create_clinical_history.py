# -*- coding: utf-8 -*-

from odoo import api, models, fields
from datetime import datetime


class CreateClinicalHistory(models.TransientModel):
    _name = 'clinical.history.wizard'
    _description = 'Clinical history of patients'

    name = fields.Many2one(
        'res.partner', string='Patient', required=True)
    date = fields.Date(string='Date', default=datetime.today())
    disease_ids = fields.Many2many(
        'pharmacy.disease.details', string="Disease", required=True)
    medicine_ids = fields.Many2many(
        'product.product', string="Medicines")

    def action_create_clinical_history_wizard(self):
        vals = {'name': self.name.id,
                'date': self.date,
                'disease_ids': [(6, 0, self.disease_ids.ids)],
                'medicine_ids': [(6,0, self.medicine_ids.ids)]}
        self.env['pharmacy.clinical.history'].create(vals)
