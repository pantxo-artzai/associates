# -*- coding: utf-8 -*-
{
    'name': "Associates",
    'summary': """
        Efficiently manage your company's associates with the Associates Management module.""",
    'description': """
        The Associates Management module provides a comprehensive solution for managing the associates 
        of your company. With this module, you can easily manage the issuance and transfer of shares, record 
        the actions and participation of your associates, and organize and conduct general meetings. You can 
        also manage the associate registry, track associate voting rights and entitlements, and generate 
        accurate reports on associate activities.""",
    'author': "Franck Patissier",
    'website': "",
    'category': 'Human Resources',
    'version': '0.1',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/view_legal_form_view.xml',
        'views/view_shares_wizard_form.xml',
        'views/distribute_dividends_wizard.xml',
        'views/update_associate_wizard.xml',
        'views/wizard_update_percentage_view.xml',
        'views/view_shares.xml',
        'views/view_shares_type.xml',
        'views/view_dashboard.xml',
        'views/view_associates.xml',
        'views/view_dividends.xml',
        'views/company_extension_view.xml',
        'report/report_associate_list_qweb.xml',
        'report/report_view.xml',
        'data/data.xml',
        'data/actions.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
