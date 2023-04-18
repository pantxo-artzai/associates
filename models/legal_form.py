from odoo import models, fields

class LegalForm(models.Model):
    _name = 'associates.legal_form'
    _description = 'Legal Form'

    name = fields.Char(string='Legal Form', required=True)
    country_id = fields.Many2one('res.country', string='Country')

