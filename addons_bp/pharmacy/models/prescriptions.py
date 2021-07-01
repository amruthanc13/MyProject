# -*- coding: utf-8 -*-

from odoo import models, fields

class Prescription(models.Model):
    _name = 'precscription'

    prescription_id = fields.Char(string="Prescription id", required=True)
    prescription_date = fields.Date(string='Prescription date')
    medicine_code = fields.char(string="Medicine")
    quantity = fields.Integer(string = 'Quantitiy')
    

