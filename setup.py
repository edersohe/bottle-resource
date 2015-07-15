from setuptools import setup

requirements = open('requirements.txt').readlines()

setup(
    name='bottle-resource',
    version='0.0.1b',
    author='Eder Sosa',
    author_email='eder.sohe@gmail.com',
    description='Bottle resource help to build resource APIs',
    py_modules=['bottle_resource'],
    install_requires=requirements,
    license='MIT',
    url='https://github.com/edersohe/bottle-resource.git'
)
