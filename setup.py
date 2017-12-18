from distutils.core import setup

setup(
    name='bitfeed',
    version='0.1.0',
    author='Bopo Wang',
    author_email='ibopo@126.com',
    packages=['bitfeed'],
    url='https://github.com/bopo/bitfeed/',
    license='LICENSE.txt',
    description='Crypto Currency Cxchange Market data feeder.',
    entry_points={
            'console_scripts': ['bitfeed=bitfeed.bitfeed:main']
        },
    install_requires=[
            'pymysql',
            'websocket-client',
            'numpy',
            'qpython',
            'pyzmq'
        ]
    )
