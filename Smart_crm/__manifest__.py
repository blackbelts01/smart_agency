# -*- coding: utf-8 -*-
{
    'name': "Smart Crm",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Black_Belts",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['crm','smart_policy'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/proposals.xml',
        'views/insurer_partner_crm.xml',

        'views/views.xml',

        # 'views/objectsview.xml',
        # 'views/templates.xml',
        # 'security/sec.xml',
        # 'reports/report_example.xml',
        # 'reports/template.xml',


    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}