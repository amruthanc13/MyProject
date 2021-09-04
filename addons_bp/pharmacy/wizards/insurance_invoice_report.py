# -*- coding: utf-8 -*-

from dateutil import relativedelta
from odoo import models, fields
from datetime import datetime


class InvoiceReportWizard(models.TransientModel):
    _name = 'insurance.invoice.report.wizard'
    _description = 'Insurance invoice report'

    insurance_company_id = fields.Many2one(
        'res.partner', string='Insurance Company')
    date_from = fields.Date(string="Date From", default=datetime.today()- relativedelta.relativedelta(months=1))
    date_to = fields.Date(string="Date To", default=datetime.today())

    def action_insurance_invoice_report_wizard(self):

        domain =[]
        insurance_id = self.read()[0].get('insurance_company_id')
        domain += [('partner_id', '=',insurance_id[0])]
        print("insurance_id is ***********",insurance_id)
        print("form data is *********",self.read()[0])
        date_from = self.date_from
        domain += [('date', '>=',date_from)]
        date_to = self.date_to
        domain += [('date', '<=',date_to)]
        
        invoices = self.env['account.move'].search_read(domain)
        print("invoices are**********",invoices)
        data = {
            'form' : self.read()[0],
            'invoices': invoices
        }
        print("form data is *********",self.read()[0])
        return self.env.ref('pharmacy.report_insurance_invoice').report_action(self, data=data)
