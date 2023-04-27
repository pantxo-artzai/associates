from odoo import models, api, _

class UpdatePercentageWizard(models.TransientModel):
    _name = 'associates.update_percentage_wizard'
    _description = 'Update Percentage Wizard'

    def update_percentage(self):
        self.env['associates.associate'].update_all_associates_percentage()
        message = _("The share percentage has been updated for all associates.")
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": _("Success"),
                "message": message,
                "sticky": False,
                "type": "success",
            },
        }
