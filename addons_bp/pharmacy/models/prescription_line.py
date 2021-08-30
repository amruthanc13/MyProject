# -*- coding: utf-8 -*-
from odoo import models, fields


class SaleOrderLineInherit(models.Model):
    _inherit = 'sale.order.line'

    def _prepare_invoice_line_with_copayment(self,copayment=None, is_customer_invoice='False', **optional_values):
        res = self._prepare_invoice_line()
        if(is_customer_invoice):
            res['price_unit'] = self.price_unit *copayment/100
        else:
            res['price_unit'] = self.price_unit *(100-copayment)/100
            res['quantity'] = self.product_uom_qty 
        return res

    def _get_to_invoice_qty(self): 
        super(SaleOrderLineInherit, self)._get_to_invoice_qty()
        for line in self:
            if line.qty_to_invoice < 0:
                line.qty_to_invoice =0

    def _get_invoice_qty(self):
        super(SaleOrderLineInherit, self)._get_invoice_qty()
        for line in self:
            if line.qty_invoiced > line.product_uom_qty:
                line.qty_invoiced = line.product_uom_qty

