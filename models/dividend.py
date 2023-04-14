from odoo import models, fields, api
from odoo.tools.translate import _
    
class dividend(models.Model):
    _name = 'associates.dividend'
    _inherit = 'mail.thread'
    _description = 'dividend'

    display_name = fields.Char(string='dividend', compute='_compute_display_name')
    sequence = fields.Char(string='dividend Reference', required=True, copy=False, readonly=True, default=lambda self: _('New'))
    associate_id = fields.Many2one(comodel_name='associates.associate', string='Associate', required=True)
    number = fields.Integer(string='dividend Number')
    value = fields.Float(string='dividend Value')
    total_value = fields.Float(string='Total Value')
    company_id = fields.Many2one(comodel_name='res.company', string='Company', default=lambda self: self.env.company)

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