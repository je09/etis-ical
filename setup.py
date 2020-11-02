from setuptools import setup

setup(
    name='etis-ical',
    version='0.9',
    packages=['src'],
    url='https://github.com/je09/etis-ical',
    license='MIT',
    author='je09',
    author_email='',
    description='',
    install_requires=[
        'click==7.1.2',
        'beautifulsoup4==4.9.3',
        'lxml==4.6.1'
    ],
    entry_points={
        'console_scripts': [
            'etis = src.main:main'
        ]
    },
)
