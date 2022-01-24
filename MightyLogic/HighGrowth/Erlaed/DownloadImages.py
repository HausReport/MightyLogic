import os
import urllib.request
from pathlib import Path

from MightyLogic.Heroes.Hero import Hero
from MightyLogic.Heroes.HeroDirectory import HeroDirectory

hd = HeroDirectory.default()

objs = hd.values()
heroes = []
for obj in objs:
    heroes.append(obj.name)
# heroes = ['Charon, Soul Catcher']
print("BLABLA" + str(os.getcwd()))
for hero in heroes:

    aName = hero
    aName = aName.replace(' ', '_')  # need to replace spaces with underline
    aName = aName.replace('"', '')  # need to replace spaces with underline
    # aName += '.png'
    if aName.endswith('rmun_Grand'):
        aName = "J%3Frmun_Grand"
    if aName.endswith('tunn'):
        aName = "J%3Ftunn"

    #
    # Create filename
    #
    bName = aName + ".png"
    path = Path.cwd() / ".." / ".." / "image" / bName
    print(path)

    if not path.exists():
        #
        # get the image
        #
        url = Hero._icon_url(aName)
        print(url)
        img = urllib.request.urlopen(url=url).read()

        #
        # save it locally
        #

        file = open(path, 'wb')
        file.write(img)
        file.close()
