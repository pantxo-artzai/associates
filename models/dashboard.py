from odoo import models, fields, api

class Dashboard(models.Model):
    _name = 'associates.dashboard'
    _description = 'Dashboard'

    name = fields.Char(string='Name')
    card_title = fields.Char(string='Card Title', translate=True)
    card_description = fields.Char(string='Card Description', translate=True)
    button_title =  fields.Char(string='Button Title', translate=True)
    button_action = fields.Many2one('ir.actions.actions', string='Button Action')

    category = fields.Selection([
    ('associates', 'Associates'),
    ('shares', 'Shares'),
    ('capital', 'Capital'),
    ], string='Category')

