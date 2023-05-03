# -*- coding: utf-8 -*-
{
    'name': "Legal form",
    'summary': """
        Legal form in company's information.""",
    'description': """
        Add a new field in the company's information section for legal forms. You can find your legal form classified by country and add a custom one.""",
    'author': "Franck Patissier",
    'website': "",
    'category': 'Technical',
    'version': '0.1',
    'license': 'GPL-3',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/company_extension_view.xml',
        'data/data.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
