from distutils.core import setup
 
setup(
    name='PyROOTUtils',
    version='1.0.1',
    packages=['PyROOTUtils', ],
    license='LICENSE',
    description='Python utilities for ROOT.',
    long_description=open('README.md').read(),
    author='Sven Kreiss, Kyle Cranmer',
    author_email='sk@svenkreiss.com',
    install_requires=[],
    entry_points={
        'console_scripts': [
        ]
    }
)
