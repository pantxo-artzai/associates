from odoo import models, fields, api

class Dashboard(models.Model):
    _name = 'associates.dashboard'
    _description = 'Dashboard'

    name = fields.Char(string='Name')
    card_title = fields.Char(string='Card Title')
    card_description = fields.Char(string='Card Description')
    button_title =  fields.Char(string='Button Title')
    button_action = fields.Many2one('ir.actions.actions', string='Button Action')
