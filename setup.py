from setuptools import setup
setup(
    name='group2_final_project',
    version='0.1.1',
    description='cli assistant to save and manage adressbook and notes',
    author='group2_GoIt_students',
    py_modules=['group2.addressbook', 'group2.birthday_functions', 'group2.main', 'group2.notebook', 
    'group2.service_addressbook', 'group2.servicenote', 'group2.sort', 'group2.terminal_tips','group2.help_func'],
    install_requires=['prompt_toolkit'],
    entry_points={
        'console_scripts': [
            'pj1=group2.main:main',
        ],
    },
    exclude_package_data={'': ['*.bin']}
)
