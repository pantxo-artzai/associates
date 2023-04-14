from odoo import models, fields, api

class Dashboard(models.Model):
    _name = 'associates.dashboard'
    _description = 'Dashboard'

    name = fields.Char(string='Name')
