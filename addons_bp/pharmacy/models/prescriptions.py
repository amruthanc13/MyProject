# -*- coding: utf-8 -*-

from odoo import models, fields


class PharmacyPrescription(models.Model):
    _name = 'pharmacy.prescription'
    _description = 'Prescription details'

    patient_name = fields.Many2one(
        'pharmacy.patient', string='Patient Name')
    prescription_date = fields.Date(string='Prescription date')
    disease = fields.Char(string='Disease')
    medicine_code = fields.Many2many('product.template', string="Medicine")
    sale_order_id = fields.Many2one(
        'pharmacy.sale.order', string='Sale order Id')
    notes = fields.Text(string='Notes')
