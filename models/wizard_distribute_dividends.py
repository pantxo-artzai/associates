from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo import _

class DistributeDividendsWizard(models.TransientModel):
    _name = 'distribute.dividends.wizard'
    _description = 'Distribute Dividends Wizard'

    dividends_total_amount = fields.Float(string='Total Dividends Amount', required=True)
    dividends_amount_by_share = fields.Float(string='Amount by share', required=True)
    date = fields.Date(string='Date', required=True, default=fields.Date.context_today)
    custom_code = fields.Text(string='Code de calcul personnalisé', related="share_type_id.custom_code")
    share_type_description = fields.Text(string='Note', related="share_type_id.description")

    share_type_id = fields.Many2one("associates.share.type", string="Share type", required=True)

    dividends_type_calcul = fields.Selection([
        ('dividends_total_amount', 'Total dividends amount calcul'),
        ('dividends_amount_by_share', 'Amount by share calcul'),
        ], string='Type', default='dividends_total_amount', required=True)

    @api.onchange('dividends_total_amount')
    def _onchange_dividends_total_amount(self):
        if self.dividends_total_amount:
            associates = self.env['associates.associate'].search([])
            for associate in associates:
                associate._compute_share_percentage()

    def button_distribute(self):
        associates = self.env['associates.associate'].search([('share_type_id', '=', self.share_type_id.id)])
        for associate in associates:
            # Calculs par défaut
            if self.dividends_type_calcul == 'dividends_total_amount':
                dividend_amount = self.dividends_total_amount * associate.share_percentage / 100
            elif self.dividends_type_calcul == 'dividends_amount_by_share':
                dividend_amount = associate.share_numbers * self.dividends_amount_by_share

            # Calculs personnalisés
            custom_code = associate.share_type_id.custom_code
            if custom_code:
                local_variables = {
                    'associate': associate,
                    'dividend_amount': dividend_amount,
                    'dividends_total_amount': self.dividends_total_amount,
                    'dividends_amount_by_share': self.dividends_amount_by_share,
                    'usufructuary_share_percentage': associate.usufructuary_share_percentage,
                    'bare_ownership_share_percentage': associate.bare_ownership_id.share_percentage,
                    'bare_ownership_share_numbers': associate.bare_ownership_id.share_numbers,

                }
                try:
                    exec(custom_code, None, local_variables)
                    dividend_amount = local_variables.get('dividend_amount', dividend_amount)
                except Exception as e:
                    raise UserError(_('Erreur dans le code personnalisé : %s') % str(e))

            self.env['associates.dividend'].create({
                'associate_id': associate.id,
                'value': dividend_amount,
                'total_value': dividend_amount,
                'company_id': self.env.company.id
            })
        return {'type': 'ir.actions.act_window_close'}


