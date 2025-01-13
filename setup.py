from setuptools import setup, find_packages

setup(
    name='ConsultaBCB',
    version='0.1',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'requests',
        'python-dotenv',
        'pyodbc',
        'pandas',
        'urllib3',
    ],
)