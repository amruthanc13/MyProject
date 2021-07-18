# -*- coding: utf-8 -*-

from odoo import api, models, fields


class DiseaseDetailsHistory(models.Model):
    _name = 'pharmacy.disease.details'
    _description = 'Disease details'

    code = fields.Char(string='Disease Code', required=True)
    name = fields.Char(string='Disease name', required=True)
    reaction_medicines = fields.Many2many(
        'product.template', string='Reaction medicines')
    disease_categ = fields.Many2one(
        'pharmacy.disease.category', string='Disease Category', required=True)


class DiseaseCategory(models.Model):
    _name = "pharmacy.disease.category"
    _description = "Disease Category"
    _parent_name = "parent_id"
    _parent_store = True
    _rec_name = 'complete_name'
    _order = 'complete_name'

    name = fields.Char('Name', index=True, required=True)
    complete_name = fields.Char(
        'Complete Name', compute='_compute_complete_name',
        store=True)
    parent_id = fields.Many2one(
        'pharmacy.disease.category', 'Parent Category', index=True, ondelete='cascade')
    parent_path = fields.Char(index=True)
    child_id = fields.One2many(
        'pharmacy.disease.category', 'parent_id', 'Child Categories')

    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for category in self:
            if category.parent_id:
                category.complete_name = '%s / %s' % (
                    category.parent_id.complete_name, category.name)
            else:
                category.complete_name = category.name
