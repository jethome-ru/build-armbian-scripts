#!/usr/bin/python
import json
import sys
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

with open(os.path.join(__location__, 'brand.json')) as json_file:
    brand = json.load(json_file)

with open(os.path.join(__location__, 'platforms.json')) as json_file:
    platforms = json.load(json_file)

with open(os.path.join(__location__, 'channels.json')) as json_file:
    channels = json.load(json_file)

with open(os.path.join(__location__, 'releases.json')) as json_file:
    releases = json.load(json_file)

with open(os.path.join(__location__, 'branches.json')) as json_file:
    branches = json.load(json_file)

'''
IMAGENAMEBURN="Armbian_${VERSION}_${BOARD^}_${RELEASE}_${BRANCH}_${LINUXVER}.burn.img.xz"
Armbian_22.05.0-trunk.0066.jethome.0_Jethubj100_bullseye_edge_5.17.5.img.xz
'''

'''
fwjson.py os platform channel release branch version
'''
if len(sys.argv) - 1 > 4:
    os = sys.argv[1]
    platform = sys.argv[2]
    channel = sys.argv[3]
    release = sys.argv[4]
    branch = sys.argv[5]
else:
    exit(-1)

mlist = []
if brand:
    plat = platforms[platform]
    #print (i, platform)
    # fw types tree
    fwtypearmbian = {
        "slug": "armbian",
        "name": "Armbian",
        "final": False,
        "is_active": True,
        "subtypes": []
    }
    if channel in channels.keys():
        fwtypechannel = channels [channel] # release,rc,nightly
    else:
        fwtypechannel = channels ['nightly'] # release,rc,nightly
        fwtypechannel['name'] = 'Nightly branch: '+ channel
        fwtypechannel['slug'] = channel

    fwtyperelease = releases [release] # focal,jammy,bulseye
    fwtypebranches = branches[branch] # current, edge

    fwtyperelease['subtypes'] = [fwtypebranches]
    fwtypechannel['subtypes'] = [fwtyperelease]
    fwtypearmbian['subtypes'] = [fwtypechannel]
    plat['firmware_types'] = [fwtypearmbian]
    brand["platforms"] = brand["platforms"] + [plat]
    mlist = mlist + [brand]
print (json.dumps(mlist,sort_keys=True, indent=4))
