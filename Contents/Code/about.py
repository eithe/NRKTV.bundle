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

from util import *

@route(pluginRoute('/about'))
def AboutMenu():
    oc = ObjectContainer()

    oc.add(PopupDirectoryObject(
            key = Callback(DoNothing),
            title=unicode(L("aboutapp_title")),
            summary=unicode(L("aboutapp_description")),
            thumb=''))

    oc.add(PopupDirectoryObject(
            key = Callback(DoNothing),
            title=unicode(L("disclaimer_title")),
            summary=unicode(L("disclaimer_description")),
            thumb=''))

    oc.add(PopupDirectoryObject(
            key = Callback(DoNothing),
            title=unicode(L("copyright_title")),
            summary=unicode(L("copyright_description")),
            thumb=''))

    oc.add(PopupDirectoryObject(
            key = Callback(DoNothing),
            title=unicode(L("ack_title")),
            summary=unicode(L("ack_description")),
            thumb=''))
    
    return oc