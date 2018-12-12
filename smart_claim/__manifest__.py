# -*- coding: utf-8 -*-
{
    'name': "Smart Claim",
    'summary': """Claim Management & Operations""",
    'description': """Insurance Broker System """,
    'author': "Black Belts Egypt",
    'website': "www.blackbelts-egypt.com",
    'category': 'Claim',
    'version': '0.1',
    'license': 'AGPL-3',
    # any module necessary for this one to work correctly
    'depends': ['base','smart_policy','mail'],

    # always loaded
    'data': [
        'security/security.xml',
        'views/claimform_view.xml',
        'views/settlements.xml',
        'views/partner.xml',
        'views/claim_menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
