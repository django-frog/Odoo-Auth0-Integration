# -*- coding: utf-8 -*-
{
    'name': 'Auth0 Login Integration',
    'version': '1.0',
    'category': 'Authentication',
    'summary': 'Login to Odoo using Auth0 SSO',
    'depends': ['base', 'web'],
    'data': [
        'views/login_button.xml',
    ],
    'installable': True,
    'application': False,
}
