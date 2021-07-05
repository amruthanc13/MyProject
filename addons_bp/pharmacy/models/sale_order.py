# -*- coding: utf-8 -*-

from odoo import models, fields


class PharmacySaleOrder(models.Model):
    _name = 'pharmacy.sale.order'

    patient_name = fields.Many2one('pharmacy.patient', string='Patient')
    prescription_id = fields.One2many(
        'pharmacy.prescription', 'id', string='Prescription id')
    medicine_code = fields.Many2many('product.product', string='Medicine')
    quantity = fields.Integer(string='Quantity')
