# -*- coding: utf-8 -*-
{
    'name': "CRM Customization",

    'summary': """
       CRM Customization
     
       """,

    'description': """
     CRM Customization
    """,

    'author': "HAK Technologies",
    'website': "http://www.haktechnologies.com",
    'license': 'OPL-1',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '16.0',

    # any module necessary for this one to work correctly
    'depends': ['stock','sale','crm'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        #'security/security.xml',
        'views/crm_deal_eval.xml',


    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
