from odoo import models, fields, api
from odoo.tools.translate import _

class Dashboard(models.Model):
    _name = 'associates.dashboard'
    _description = 'Dashboard'
    
    name = fields.Char(string="Titre", required=True)
    description = fields.Text(string="Description")
    bouton = fields.Char(string="Bouton")