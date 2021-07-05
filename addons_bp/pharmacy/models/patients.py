# -*- coding: utf-8 -*-

from odoo import models, fields


class PharmacyPatient(models.Model):
    _name = 'pharmacy.patient'

    patient_first_name = fields.Char(string='First name', required=True)
    patient_last_name = fields.Char(string='Last name', required=True)
    age = fields.Integer(string='Age')
    prescription_id = fields.One2many(
        'pharmacy.prescription', 'id', string='Prescription id')
    gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    clinical_History = fields.One2many(
        'pharmacy.clinical.history', 'id', string="Clinical History")
    email = fields.Char(string='Email id')
    address = fields.Char(string='Address', required=True)
    contact = fields.Char(string='Contact No.')
    sale_order = fields.One2many(
        'pharmacy.sale.order', 'id', string="Sale order")
    note = fields.Text(string='Notes')
    image = fields.Binary(string='Image')
