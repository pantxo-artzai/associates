from odoo import models, fields, api
from odoo.tools.translate import _

class Share(models.Model):
    _name = 'associates.share'
    _inherit = 'mail.thread'
    _description = 'Share'

    display_name = fields.Char(string='Share', compute='_compute_display_name')
    sequence = fields.Char(string='Share Reference', required=True, copy=False, readonly=True, default=lambda self: _('New'))
    associate_id = fields.Many2one(comodel_name='associates.associate', string='Associate', required=True)
    value = fields.Float(string='Share Value')
    company_id = fields.Many2one(comodel_name='res.company', string='Company', default=lambda self: self.env.company)
    subscription_date = fields.Date(string='Subscription Date')
    share_type_id = fields.Many2one(comodel_name='associates.share.type', string='Share Type')


    @api.model

    def create(self, vals):
        if vals.get('sequence', _('New')) == _('New'):
            vals['sequence'] = self.env['ir.sequence'].next_by_code('associates.share.sequence') or _('New')
        result = super(Share, self).create(vals)
        return result
    
    def name_get(self):
        result = []
        for record in self:
            name = "%s" % (record.sequence)
            result.append((record.id, name))
        return result

class ShareType(models.Model):
    _name = 'associates.share.type'
    _description = 'Share Type'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    country_id = fields.Many2one(comodel_name='res.country', string='Country')


