# -*- coding: utf-8 -*-

from odoo import api, models, fields
class MedicineProductInherit(models.Model):
    _inherit = 'product.template'

    medicine_code = fields.Char(string='International drug code')
    prescription_required = fields.Boolean(string='Prescription Required', default=False)

    @api.onchange('prescription_required')
    def _onchange_prescription_required(self):
        if self.prescription_required :
            self.available_in_pos = False
