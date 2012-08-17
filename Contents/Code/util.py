# -*- coding: utf-8 -*-

# "THE BEER-WARE LICENSE" (Revision 42):
# <eithe@plexforums> wrote this file.  As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return. Eirik H.

# Some of this stuff is from:
# jonklo's NRK Plex plugin: https://github.com/plexinc-plugins/NRK.bundle
# takoi's NRK XBMC plugin: https://github.com/takoi/xbmc-addon-nrk
# Please comply with their licenses, I haven't looked at them yet.

# NRK, if you are watching, don't hesitate to make contact.

VIDEO_PREFIX = "/video/nrk"

NAME = unicode(L('title'))

BASE_URL = "http://tv.nrk.no"
RESOLUTIONS = ["180","SD","480","720","1080"]
# make sure to replace artwork with what you want
# these filenames reference the example files in
# the Contents/Resources/ folder in the bundle
ART_DEFAULT  = 'art-default.png'
ICON_DEFAULT = 'icon-default.png'

def pluginRoute(route):
    return VIDEO_PREFIX + route

@route(pluginRoute('/dev/null'))
def DoNothing():
    return

def emptyItem():
    return PopupDirectoryObject(
            key = Callback(DoNothing),
            title=unicode(L("empty_title")),
            summary=unicode(L("empty_description")),
            thumb='')