from odoo import api, fields, models

class UpdateAssociateWizard(models.TransientModel):
    _name = "associates.update_associate_wizard"
    _description = 'Upadte associate wizard for share tansfert'


    new_associate_id = fields.Many2one("associates.associate", string="New Associate", required=True)

    def update_shares(self):
        share_ids = self.env.context.get("share_ids")
        if share_ids:
            shares = self.env["associates.share"].browse(share_ids)
            shares.write({"associate_id": self.new_associate_id.id})
        return {"type": "ir.actions.act_window_close"}
