# -*- coding: utf-8 -*-
from odoo import api, models, fields


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    disease_ids = fields.Many2many(
        'pharmacy.disease.details', string='Diseases')

    def action_confirm(self):
        super(SaleOrderInherit, self).action_confirm()
        if self.state == 'sale' and self.diseases.exists():
            vals = {'name': self.partner_id.id,
                    'date': self.date_order,
                    'diseases': [(6, 0, self.diseases.ids)]}
            self.env['pharmacy.clinical.history'].create(vals)
        return True
