{
    'name': 'HMS',
    'version': '1.0',
    'depends': ['base', 'contacts'],
    'data': [
        'views/patient_views.xml',
        'views/department_views.xml',
        'views/doctor_views.xml',
        'security/hms_security.xml',
        'security/hms_rules.xml',
        'security/ir.model.access.csv',
        'reports/patient_report.xml',
        'reports/patient_report_template.xml',
    ],
    'installable': True,
    'application': True,
    
}