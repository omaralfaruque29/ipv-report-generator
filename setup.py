from setuptools import setup

with open("README", 'r') as f:
    long_description = f.read()

setup(
   name='report generation',
   version='1.0',
   description='wonderful report generation',
   license="MIT",
   long_description=long_description,
   author='ipv-cloud-team',
   author_email='raselashraf21@gmail.com',
   url="http://www.foopackage.com/",
   packages=['ipv-report-generation'],
)