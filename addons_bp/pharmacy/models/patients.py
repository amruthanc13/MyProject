# -*- coding: utf-8 -*-

from odoo import models, fields

class Patient(models.Model):
    _name = 'patient'

    patient_name = fields.Char(string="Patient name", required=True)
    age = fields.Integer(string="Age")
    prescription_id = fields.Char(string="Prescription id", required=True)
    clinical_History = fields.Char(string="Clinical History", required=True)
    email = fields.Char(string="Email id", required=True)
    address = fields.Char(string="Address", required=True)
    contact = fields.Char(string="contact", required=True)