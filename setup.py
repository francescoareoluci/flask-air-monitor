from setuptools import setup, find_packages

requires = [
    'flask',
    'flask-sqlalchemy',
    'psycopg2',
    'datetime',
    'pytz',
    'requests',
    'csv',
    'json'
]

setup(
    name='flask-air-monitor',
    version='1.0',
    description='A simple dev server for air monitor project',
    author='Francesco Areoluci',
    author_email='francesco.areoluci@gmail.com',
    keywords='web flask',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires
)
