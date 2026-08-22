import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo14-addons-open-synergy-ssi-school-extracurricular",
    description="Meta package for open-synergy-ssi-school-extracurricular Odoo addons",
    version=version,
    install_requires=[
        'odoo14-addon-ssi_school_extracurricular',
        'odoo14-addon-ssi_school_extracurricular_operating_unit',
        'odoo14-addon-ssi_school_extracurricular_session',
        'odoo14-addon-ssi_school_extracurricular_session_operating_unit',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 14.0',
    ]
)
