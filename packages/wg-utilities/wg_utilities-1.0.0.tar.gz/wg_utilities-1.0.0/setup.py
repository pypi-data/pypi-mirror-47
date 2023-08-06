from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

setup(
    name='wg_utilities',
    version='1.0.0',
    author='Will Garside',
    author_email='worgarside@gmail.com',
    description='Utilities for using in personal projects.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/worgarside/wg-utilities',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=['requests', 'httplib2', 'google-api-python-client']
)
