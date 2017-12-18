# from distutils.core import setup
from setuptools import setup, find_packages
from bitfeeds import __version__

setup(
    name='bitfeeds',
    version=__version__,
    author='Bopo Wang',
    author_email='ibopo@126.com',
    url='https://github.com/bopo/bitfeeds/',
    license='LICENSE.txt',
    description='Crypto Currency Cxchange Market data feeder.',
    entry_points={
            'console_scripts': ['bitfeeds=bitfeeds.bitfeeds:main']
        },
    install_requires=[
            'websocket-client',
            'qpython',
            'pymysql',
            'numpy',
            'pyzmq'
        ],
    packages=find_packages(exclude=('tests', 'docs')),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ]       
)
