from odoo import models, fields, api
from odoo.tools.translate import _

class Associate(models.Model):
    _name = 'associates.associate'
    _inherit = 'mail.thread'
    _description = 'Associate'

    name = fields.Char(string='Name')
    email = fields.Char(string='Email', related='partner_id.email')
    phone = fields.Char(string='Phone', related='partner_id.phone')
    birth_date = fields.Date(string='Birthdate')
    nationality = fields.Many2one('res.country', string='Nationality', required=True)
    street = fields.Char(string='street', related='partner_id.street')
    street2 = fields.Char(string='street2', related='partner_id.street2')
    city = fields.Char(string='city', related='partner_id.city')
    state_id = fields.Many2one(string='state_id', related='partner_id.state_id')
    zip = fields.Char(string='zip', related='partner_id.zip')
    country_id = fields.Many2one(string='Counry', related='partner_id.country_id')
    notes = fields.Text(string='Notes')

    shares_amount = fields.Float(string="Shares total amount", compute="_compute_shares_amount", store=True)
    share_count = fields.Integer(string='Shares', compute='_compute_share_count',store=True, tracking=1)
    share_numbers = fields.Integer(string='Shares numbers', compute='_compute_share_count',store=True, tracking=1)
    share_percentage = fields.Float(string="Share percentage", compute="_compute_share_percentage", store=True, tracking=1)
    share_numbers = fields.Integer(string='Shares numbers', compute='_compute_share_count',store=True, tracking=1)
    
    dividend_count = fields.Integer(compute='_compute_dividend_count', string='Dividend Count')

    membership_start_date = fields.Date(string='Start date', tracking=1)
    membership_end_date = fields.Date(string='End date', tracking=1)

    partner_id = fields.Many2one('res.partner', string='Related Contact', required=True, tracking=1)
    company_id = fields.Many2one("res.company", string="Company", required=True, default=lambda self: self.env.company, tracking=1)
    share_type_id = fields.Many2one('associates.share.type', string='Default share type', required=True, tracking=1)
    bare_ownership_id = fields.Many2one('associates.associate', string='Bare Ownership', readonly=True)
    dividend_ids = fields.One2many('associates.dividend', 'associate_id', string='Dividends')

    share_ids = fields.One2many(
        'associates.share', 'associate_id', string='Shares', tracking=1
        )
    usufructuary_ids = fields.Many2many(
        "associates.associate", "associate_rel", "main_id", "other_id", string="Usufructuaries",
        domain=[('type', '=', 'usufructuaries')]
        )

    type = fields.Selection([
        ('full_ownership', 'Full ownership'),
        ('bare_ownership', 'Bare ownership'),
        ('usufructuaries', 'Usufructuaries')
        ], string='Type')

    state = fields.Selection([
        ('new', 'New'),
        ('in_progress', 'In progress'),
        ('validated', 'Validated'),
        ('archived', 'Archived'),
        ], string='Status', readonly=False, default='new')

    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
        ], string='Gender')

    @api.depends('usufructuary_ids')
    def _compute_bare_ownership_id(self):
        for record in self:
            main_associates = self.env['associates.associate'].search([('usufructuary_ids', 'in', record.id)])
            if main_associates:
                record.bare_ownership_id = main_associates[0]
            else:
                record.bare_ownership_id = False

    @api.model
    def create(self, vals):
        # Update the name based on the partner_id
        name = self.env['res.partner'].browse(vals['partner_id']).name
        vals.update({'name': name})

        record = super(Associate, self).create(vals)

        # Update the bare_ownership_id for the associated records
        if 'usufructuary_ids' in vals:
            for associate_id in vals['usufructuary_ids'][0][2]:
                associate = self.env['associates.associate'].browse(associate_id)
                associate.bare_ownership_id = record.id

        return record

    def write(self, vals):
        # Store the current values of usufructuary_ids for each record
        current_usufructuary_ids = {record.id: record.usufructuary_ids.ids for record in self}

        res = super(Associate, self).write(vals)

        if 'usufructuary_ids' in vals:
            for record in self:
                added_ids = set(vals['usufructuary_ids'][0][2]) - set(current_usufructuary_ids[record.id])
                removed_ids = set(current_usufructuary_ids[record.id]) - set(vals['usufructuary_ids'][0][2])

                for associate_id in added_ids:
                    associate = self.env['associates.associate'].browse(associate_id)
                    associate.bare_ownership_id = record.id

                for associate_id in removed_ids:
                    associate = self.env['associates.associate'].browse(associate_id)
                    associate.bare_ownership_id = False

        return res

    def update_all_associates_percentage(self):
        associates = self.search([])
        for associate in associates:
            total_shares = self.env["associates.share"].search_count([('company_id', '=', associate.company_id.id)])
            associate_shares = len(associate.share_ids)
            if total_shares > 0:
                associate.share_percentage = (associate_shares / total_shares) * 100
            else:
                associate.share_percentage = 0.0

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
        action = self.env.ref("associates.action_create_shares_wizard").read()[0]
        action["context"] = {
            "default_associate_id": self.id,
            "default_associate_name": self.name,
        }
        return action
    
    def action_in_progress(self):
        for record in self:
            record.state = 'in_progress'

    def action_validate(self):
        for record in self:
            record.state = 'validated'

    def action_archived(self):
        for record in self:
            record.state = 'archived'

    def action_new(self):
        for record in self:
            record.state = 'new'
    
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

    @api.depends('dividend_ids')
    def _compute_dividend_count(self):
        for associate in self:
            associate.dividend_count = len(associate.dividend_ids)

