# -*- coding: utf-8 -*-

from odoo import models, fields


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    diseases = fields.Many2many('pharmacy.disease.details', string='Disease')
