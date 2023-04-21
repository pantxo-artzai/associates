from odoo import api, fields, models

class DistributeDividendsWizard(models.TransientModel):
    _name = 'distribute.dividends.wizard'
    _description = 'Distribute Dividends Wizard'

    dividends_total_amount = fields.Float(string='Total Dividends Amount', required=True)
    note = fields.Text(string='Note')
    date = fields.Date(string='Date', required=True, default=fields.Date.context_today)

    @api.onchange('dividends_total_amount')
    def _onchange_dividends_total_amount(self):
        if self.dividends_total_amount:
            associates = self.env['associates.associate'].search([])
            for associate in associates:
                associate._compute_share_percentage()

    def button_distribute(self):
        associates = self.env['associates.associate'].search([])
        for associate in associates:
            dividend_amount = self.dividends_total_amount * associate.share_percentage / 100
            self.env['associates.dividend'].create({
                'associate_id': associate.id,
                'value': dividend_amount,
                'total_value': dividend_amount,
                'number': 1,  # or any other logic for dividend number
                'company_id': self.env.company.id
            })
        return {'type': 'ir.actions.act_window_close'}
