# -*- coding: utf-8 -*-

from odoo import api, models, fields


class DiseaseDetailsHistory(models.Model):
    _name = 'pharmacy.disease.details'
    _description = 'Disease details'

    code = fields.Char(string='Disease Code', required=True)
    name = fields.Char(string='Disease name', required=True)
    reaction_medicine_ids = fields.Many2many(
        'product.product', string='Reaction medicines')
    disease_categ_id = fields.Many2one(
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
    disease_count = fields.Integer(
        '# Diseases', compute='_compute_disease_count',
        help="The number of disease under this category (Does not consider the children categories)")

    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for category in self:
            if category.parent_id:
                category.complete_name = '%s / %s' % (
                    category.parent_id.complete_name, category.name)
            else:
                category.complete_name = category.name

    def _compute_disease_count(self):
        read_group_res = self.env['pharmacy.disease.details'].read_group(
            [('disease_categ_id', 'child_of', self.ids)], ['disease_categ_id'], ['disease_categ_id'])
        group_data = dict(
            (data['disease_categ_id'][0], data['disease_categ_id_count']) for data in read_group_res)
        for categ in self:
            disease_count = 0
            for sub_categ_id in categ.search([('id', 'child_of', categ.ids)]).ids:
                disease_count += group_data.get(sub_categ_id, 0)
            categ.disease_count = disease_count
