from odoo import models, fields, api
from odoo.tools.translate import _
    
class dividend(models.Model):
    _name = 'associates.dividend'
    _inherit = 'mail.thread'
    _description = 'dividend'

    display_name = fields.Char(string='dividend', compute='_compute_display_name')
    sequence = fields.Char(string='dividend Reference', required=True, copy=False, readonly=True, default=lambda self: _('New'))
    associate_id = fields.Many2one('associates.associate', string='Associate', required=True)
    number = fields.Integer(string='dividend Number')
    value = fields.Float(string='dividend Value')
    total_value = fields.Float(string='Total Value')
    company_id = fields.Many2one(comodel_name='res.company', string='Company', default=lambda self: self.env.company)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('validated', 'Validated'),
        ('accounted', 'Accounted'),
        ('paid', 'Paid'),
        ], string='Status', readonly=True, default='draft')

    @api.model

    def create(self, vals):
        if vals.get('sequence', _('New')) == _('New'):
            vals['sequence'] = self.env['ir.sequence'].next_by_code('associates.dividend.sequence') or _('New')
        result = super(dividend, self).create(vals)
        return result
    
    def name_get(self):
        result = []
        for record in self:
            name = "%s" % (record.sequence)
            result.append((record.id, name))
        return result

    def action_validate(self):
        for record in self:
            record.state = 'validated'

    def action_account(self):
        for record in self:
            record.state = 'accounted'

    def action_pay(self):
        for record in self:
            record.state = 'paid'

    def action_draft(self):
        for record in self:
            record.state = 'draft'