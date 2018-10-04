from setuptools import setup, find_packages

setup(
    name='Git Change Log Utility Service',
    version='0.1.0',
    description='This utility is used to get change log info from git.',
    author='Anand Varne',
    author_email='avarne@digite.com',
    url='<URL>',#Give Valid URL at <URL>    keywords=["Swagger", "Git Change Log"]
    install_requires=open('requirements.txt').read(),
    packages=find_packages(),
    include_package_data=True,
    license='',
    long_description=open('README.md').read(),
	test_suite='nose.collector',
    tests_require=['nose']
)