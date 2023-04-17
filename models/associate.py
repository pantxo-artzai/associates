from odoo import models, fields, api
from odoo.tools.translate import _

class Associate(models.Model):
    _name = 'associates.associate'
    _inherit = 'mail.thread'
    _description = 'Associate'

    name = fields.Char(string='Name')
    partner_id = fields.Many2one('res.partner', string='Related Contact', required=True, tracking=1)
    company_id = fields.Many2one("res.company", string="Company", required=True, default=lambda self: self.env.company, tracking=1)
    share_ids = fields.One2many('associates.share', 'associate_id', string='Shares', tracking=1)
    share_type_id = fields.Many2one('associates.share.type', string='Default share type', required=True, tracking=1)

    email = fields.Char(string='Email', related='partner_id.email')
    phone = fields.Char(string='Phone', related='partner_id.phone')
    address = fields.Char(string='Address')
    birth_date = fields.Date(string='Birthdate')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string='Gender')
    nationality = fields.Many2one('res.country', string='Nationality', required=True)
    membership_start_date = fields.Date(string='Start date', tracking=1)
    shares_amount = fields.Float(string="Shares total amount", compute="_compute_shares_amount", store=True)
    membership_end_date = fields.Date(string='End date', tracking=1)
    notes = fields.Text(string='Notes')
    share_count = fields.Integer(string='Shares', compute='_compute_share_count',store=True, tracking=1)
    share_numbers = fields.Integer(string='Shares numbers', compute='_compute_share_count',store=True, tracking=1)
    share_percentage = fields.Float(string="Share percentage", compute="_compute_share_percentage", store=True, tracking=1)

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
            associate.share_numbers = len(associate.share_ids)

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
    
    @api.depends("share_ids", "company_id")
    def _compute_share_percentage(self):
        for associate in self:
            total_shares = self.env["associates.share"].search_count([('company_id', '=', associate.company_id.id)])
            associate_shares = len(associate.share_ids)
            if total_shares > 0:
                associate.share_percentage = (associate_shares / total_shares) * 100
            else:
                associate.share_percentage = 0.0

    @api.depends("share_ids", "share_ids.value")
    def _compute_shares_amount(self):
        for associate in self:
            shares_amount = sum(share.value for share in associate.share_ids)
            associate.shares_amount = shares_amount
