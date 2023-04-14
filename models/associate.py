from odoo import models, fields, api
from odoo.tools.translate import _

class Associate(models.Model):
    _name = 'associates.associate'
    _inherit = 'mail.thread'
    _description = 'Associate'

    name = fields.Char(string='Name')
    partner_id = fields.Many2one('res.partner', string='Related Contact', required=True)
    share_ids = fields.One2many('associates.share', 'associate_id', string='Shares')
    email = fields.Char(string='Email', related='partner_id.email')
    phone = fields.Char(string='Phone', related='partner_id.phone')
    address = fields.Char(string='Address')
    birth_date = fields.Date(string='Birthdate')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string='Gender')
    nationality = fields.Char(string='Nationality')
    joining_date = fields.Date(string='Joining Date')
    membership_type = fields.Selection([
        ('regular', 'Regular'),
        ('premium', 'Premium'),
        ('lifetime', 'Lifetime')
    ], string='Membership Type')
    shares_amount = fields.Float(string='Share Amount')
    membership_end_date = fields.Date(string='Membership End Date')
    membership_status = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('pending', 'Pending')
    ], string='Membership Status', default='active')
    notes = fields.Text(string='Notes')
    share_count = fields.Integer(string='Shares', compute='_compute_share_count')


    @api.model
    def create(self, vals):
        name = self.env['res.partner'].browse(vals['partner_id']).name
        vals.update({'name': name})
        return super(Associate, self).create(vals)
    
    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.partner_id:
            self.name = self.partner_id.name

    @api.depends('share_ids')
    def _compute_share_count(self):
        for associate in self:
            associate.share_count = len(associate.share_ids)

    def action_view_shares(self):
        action = self.env.ref('associates.action_view_share').read()[0]
        action['domain'] = [('associate_id', 'in', self.ids)]
        return action
    
    def create_shares(self):
        # Récupérer l'action pour ouvrir le formulaire de création de parts
        action = self.env.ref("associates.action_create_shares_wizard").read()[0]

        # Transmettre l'ID de l'associé actuel à l'action
        action["context"] = {
            "default_associate_id": self.id,
            "default_associate_name": self.name,
        }

        return action
