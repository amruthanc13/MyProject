# -*- coding: utf-8 -*-

from odoo import models, fields


class DiseaseDetailsHistory(models.Model):
    _name = 'pharmacy.disease.details'
    _description = 'Disease details'

    code = fields.Char(string='Disease Code', required=True)
    name = fields.Char(string='Disease name', required=True)
    reaction_medicine = fields.Many2many(
        'product.template', string='Reaction to')
