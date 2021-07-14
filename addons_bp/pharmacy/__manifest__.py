# -*- coding: utf-8 -*-
{
    'name': 'Pharmacy',
    'version': '1.1',
    'summary': 'Pharmacy management app',
    'sequence': -100,
    'description': """Application to manage multi chain pharamacy companies""",
    'category': 'Sales/Sales',
    'website': 'https://www.odoo.com/page/billing',
    'depends': ['base', 'sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/pharmacy.xml',
        'views/pharmacy_sales.xml'],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
