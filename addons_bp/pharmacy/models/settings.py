# -*- coding: utf-8 -*-

from odoo import fields, models


class PharmacySettings(models.TransientModel):
    _inherit = 'res.config.settings'

    confirmation_report = fields.Boolean(
        string='Confirmation Report', readonly=False)
    dynamic_report_template_id = fields.Many2one(
        'dynamic.report.template', string='Report Template',
        domain="[('model', '=', 'sale.order')]")

    def set_values(self):
        res = super(PharmacySettings, self).set_values()
        self.env['ir.config_parameter'].set_param(
            'pharmacy.confirmation_report', self.confirmation_report)
        if self.confirmation_report:
            self.env['ir.config_parameter'].set_param(
                'pharmacy.dynamic_report_template_id',
                self.dynamic_report_template_id.id)
        return res

    def get_values(self):
        res = super(PharmacySettings, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        confirmation_report = ICPSudo.get_param('pharmacy.confirmation_report')
        dynamic_report_id = ICPSudo.get_param(
            'pharmacy.dynamic_report_template_id')
        template_id = self.env['dynamic.report.template'].search(
            [('id', '=', dynamic_report_id)])
        res.update(
            confirmation_report=confirmation_report,
            dynamic_report_template_id=template_id
        )
        return res
