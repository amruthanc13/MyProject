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
        'data/pharmacy.disease.category.csv',
        'data/pharmacy_product_data.xml',
        'data/pharmacy_disease.xml',
        'security/ir.model.access.csv',
        'views/pharmacy_patients.xml',
        'views/pharmacy.xml',
        'views/pharmacy_sales.xml',
        'views/pharmacy_clinical_history.xml',
        'views/pharmacy_disease.xml',
        'views/pharmacy_medicine.xml'],
    'demo': [
        'demo/pharmacy_product_demo.xml',
        'demo/pharmacy_patient_demo.xml',
        'demo/pharmacy_clinical_history_demo.xml',
        'demo/pharmacy_prescription_order_demo.xml'
    ],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
