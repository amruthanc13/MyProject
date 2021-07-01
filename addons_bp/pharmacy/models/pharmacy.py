# -*- coding: utf-8 -*-

from odoo import models, fields

class Pharmacy(models.Model):
    _name = 'pharmacy'

    name = fields.Char(string="Pharmacy Name", required=True)
    location = fields.char(string="Location", required=True)

