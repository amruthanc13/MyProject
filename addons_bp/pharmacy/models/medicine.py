# -*- coding: utf-8 -*-

from odoo import models, fields


class MedicineProductInherit(models.Model):
    _inherit = 'product.product'

    medicine_code = fields.Char(string='International drug code')
