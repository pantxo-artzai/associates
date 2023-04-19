from odoo import models, fields, api
from odoo.tools.translate import _

class Share(models.Model):
    _name = 'associates.share'
    _inherit = 'mail.thread'
    _description = 'Share'

    display_name = fields.Char(string='Share', compute='_compute_display_name')
    sequence = fields.Char(string='Share Reference', required=True, copy=False, readonly=True, default=lambda self: _('New'))
    associate_id = fields.Many2one(comodel_name='associates.associate', string='Associate', required=True, tracking=1)
    value = fields.Float(string='Share Value')
    company_id = fields.Many2one(comodel_name='res.company', string='Company', default=lambda self: self.env.company)
    subscription_date = fields.Date(string='Subscription Date')
    share_type_id = fields.Many2one(string="Share Type", related="associate_id.share_type_id", readonly=True, store=True)

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
    
    def update_associate(self):
        # Ouverture du wizard pour sélectionner le nouvel associé
        wizard_form_view = self.env.ref("associates.view_update_associate_wizard_form")
        return {
            "name": "Update Associate",
            "type": "ir.actions.act_window",
            "res_model": "associates.update_associate_wizard",
            "views": [(wizard_form_view.id, "form")],
            "target": "new",
            "context": {"share_ids": self.ids},
        }

class ShareType(models.Model):
    _name = 'associates.share.type'
    _description = 'Share Type'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    country_id = fields.Many2one(comodel_name='res.country', string='Country')
    dividend_fixed = fields.Boolean(string="Fixed dividend")
    dividend_priority = fields.Boolean(string="Priority dividends")
    vote_agm = fields.Boolean(string="Vote at the Annual General Meeting (AGM)")
    vote_egm = fields.Boolean(string="Vote at the Extraordinary General Meeting (EGM)")

