# -*- coding: utf-8 -*-

from odoo import api, models, fields


class StockInherit(models.Model):
    _inherit = 'stock.scrap'

    def scrap_expired_products(self):

        lots = self.env['stock.production.lot'].search([
            ('removal_date', '<=', fields.Date.today())
        ])
        for lot in lots:
            if lot.product_qty:
                vals = {'product_id': lot.product_id.id,
                        'product_uom_id': lot.product_id.uom_id.id,
                        'scrap_qty': lot.product_qty,
                        'lot_id': lot.id}
                scrap = self.env['stock.scrap'].create(vals)
                scrap.do_scrap()
        return True
