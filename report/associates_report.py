from odoo import api, fields, models

class ReportAssociates(models.AbstractModel):
    _name = "report.assoictaes.report_associate_list_qweb"

    def _get_report_values(self, docids, data=None):
        # get the report action back as we will need its data
        report = self.env['ir.actions.report']._get_report_from_name('associates.report_associate_list_qweb')
        # get the records selected for this rendering of the report
        obj = self.env[report.model].browse(docids)
        # return a custom rendering context
        return {
            'lines': docids.get_lines()
        }