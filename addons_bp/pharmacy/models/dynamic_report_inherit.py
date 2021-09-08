# -*- coding: utf-8 -*-
import base64
from odoo import api, models, fields

class DynamicReportTemplate(models.Model):
    _inherit = "dynamic.report.template"

    def action_generate_preview(self):
        self.ensure_one()
        record = self.env[self.model].search([], limit=1)
        if not record:
            return
        pdfs = self.generate_pdf(record.ids)
        data = base64.b64encode(pdfs[record.id])

        attachment = self.env['ir.attachment'].create({
                'name': f"Preview of {self.name}.pdf",
                'res_id': record.id,
                'res_model': self._context.get('active_model'),
                'datas': data,
                'description': record.id,
                'type': 'binary',
            })
        
        base_url = self.env['ir.config_parameter'].get_param('web.base.url')
        download_url = '/web/content/' + str(attachment.id)
        return  {
	                "type": "ir.actions.act_url",
	                "url": str(base_url) + str(download_url),
	                "target": "new",
                }
