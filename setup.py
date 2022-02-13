from setuptools import setup

setup(
    name='MightyLogic',
    version='0.499995',
    include_package_data=True,
    packages=[
        'MightyLogic',
        'MightyLogic.Heroes',
        'MightyLogic.HighGrowth',
        'MightyLogic.HighGrowth.Erlaed',
        'MightyLogic.HighGrowth.Strategies',
        'MightyLogic.Player',
        'MightyLogic.Rarity',
        'MightyLogic.Rewards',
        'MightyLogic.TurfWar',
        'MightyLogic.TurfWar.Tiles',
        'MightyUseful',
        'MightyUseful.Utilities',
        'MightyUseful.PandaTables',
        'MightyUseful.HighGrowth',
        'MightyUseful.ArmyAnalyzer',
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
