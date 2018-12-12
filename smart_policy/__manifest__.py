# -*- coding: utf-8 -*-
{
    'name': "Smart Policies",
    'summary': """Policy Management & Operations""",
    'description': """Insurance Broker System """,
    'author': "Black Belts Egypt",
    'website': "www.blackbelts-egypt.com",
    'category': 'Policy',
    'version': '0.1',
    'license': 'AGPL-3',
    # any module necessary for this one to work correctly
    'depends': ['base','account','mail','sale',],

    # always loaded
    'data': [
        # 'security/security.xml',
        'views/policy_setup_view.xml',
        'views/renewal_view.xml',
        'views/policy_view.xml',
        'views/installments_view.xml',
        'views/endorsement.xml',
        'views/insured_cargo.xml',
        'views/insured_object.xml',
        'views/insured_vehicle.xml',
        'views/insurer_partner.xml',
        'views/policy_menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
