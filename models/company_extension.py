from odoo import models, fields

class ResCompany(models.Model):
    _inherit = 'res.company'

    capital = fields.Float(string="Capital")
    legal_form_id = fields.Many2one('associates.legal_form', string='Legal Form')

