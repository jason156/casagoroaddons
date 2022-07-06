{
    'name': 'User Signup Approval',
    'version': '13.0.1',
    'category': 'Extra Tools',
    'license': 'OPL-1',
    'summary': 'Ask for the approval when new user do signup',
    'description': """
        Ask for the approval when user do signup
    """,

    'author': 'Er. Vaidehi Vasani',
    'maintainer': 'Er. Vaidehi Vasani',

    'depends': ['auth_signup', 'website', 'base_setup'],
    'data': [
        'views/res_users_view.xml',
        'views/res_partner_view.xml',
        'views/thankyou_signup.xml',
        'data/signup_template_data.xml',
        'views/auth_signup_view.xml',
        'views/res_config_setting_view.xml',
        'views/template.xml'
    ],
    'images': ['images/user_signup_approval_app_coverpage.png'],

    'installable': True,
    'auto_install': False,
    'application': True,
    'price': 00.00,
    'currency': 'USD',
}
