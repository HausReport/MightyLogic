from setuptools import setup

setup(
    name='MightyLogic',
    version='0.40',
    packages=[
        'MightyLogic',
        'MightyLogic.Heroes',
        'MightyLogic.HighGrowth',
        'MightyLogic.HighGrowth.Erlaed',
        'MightyLogic.HighGrowth.Strategies',
        'MightyLogic.Player',
        'MightyLogic.Rewards',
        'MightyLogic.TurfWar',
        'MightyLogic.TurfWar.Tiles',
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
