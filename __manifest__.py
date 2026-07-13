# -*- coding: utf-8 -*-
{
    'name': 'Goals Management - Helpdesk Bridge',
    'version': '19.0.1.0.0',
    'summary': 'Vincula tickets de helpdesk con microobjetivos de Goals Management.',
    'description': """
        Módulo puente que permite asociar tickets de helpdesk a microobjetivos
        del sistema de gestión de objetivos, incluyendo su progreso en el
        cálculo de completitud del microobjetivo.
    """,
    'category': 'Productivity/Goals',
    'author': 'Aftermoves',
    'website': 'https://aftermoves.com',
    'license': 'LGPL-3',
    'depends': [
        'goals_management',
        'helpdesk',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/goals_link_ticket_wizard_views.xml',
        'views/helpdesk_ticket_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': True,
}
