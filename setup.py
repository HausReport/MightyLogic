from setuptools import setup

setup(
    name='MightyLogic',
    version='0.1',
    packages=[
        'MightyLogic',
        'MightyLogic.Heroes',
        'MightyLogic.HighGrowth',
        'MightyLogic.HighGrowth.Strategies',
        'MightyLogic.Rewards',
        'MightyLogic.TurfWar',
        'MightyLogic.TurfWar.Tiles',
        'HighGrowth'
    ],
    url='https://github.com/HausReport/MightyLogic',
    license='',
    author='Erlaed',
    author_email='Erlaed',
    description='Mighty Party utils',
    install_requires=[
        'pytest'
    ]
)
