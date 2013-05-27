# -*- coding: utf-8 -*-

# "THE BEER-WARE LICENSE" (Revision 42):
# <eithe@plexforums> wrote this file.  As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return. Eirik H.
# This version of the plugin is modified by Erling Brandvik (burnbay@plexforum)

# Some of this stuff is from:
# jonklo's NRK Plex plugin: https://github.com/plexinc-plugins/NRK.bundle
# takoi's NRK XBMC plugin: https://github.com/takoi/xbmc-addon-nrk
# Please comply with their licenses, I haven't looked at them yet.

# NRK, if you are watching, don't hesitate to make contact.

from live_tv import LiveTVMenu
from browser import *
from about import AboutMenu
from util import *

####################################################################################################

def Start():
    Plugin.AddPrefixHandler(VIDEO_PREFIX, MainMenu, NAME, ICON_DEFAULT, ART_DEFAULT)

    Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")
    Plugin.AddViewGroup("List", viewMode="List", mediaType="items")

    ObjectContainer.art = R(ART_DEFAULT)
    ObjectContainer.view_group = "InfoList"
    ObjectContainer.title1 = NAME

    EpisodeObject.art = R(ART_DEFAULT)
    EpisodeObject.thumb = R(ICON_DEFAULT)

    HTTP.CacheTime = CACHE_1HOUR

def MainMenu():
    oc = ObjectContainer()
    
    oc.add(DirectoryObject(
        key = Callback(LiveTVMenu),
        title=unicode(L('livetv_title')), 
        summary=unicode(L('livetv_description')), 
        thumb=R('nrk-nett-tv.png')))

    oc.add(DirectoryObject(
        key = Callback(LettersMenu),
        title=unicode(L('letters_title')), 
        summary=unicode(L('letters_description')), 
        thumb=R('nrk-nett-tv.png')))

    oc.add(InputDirectoryObject(
        key = Callback(SearchResults),
        title = unicode(unicode(L("search_title"))) ,
        summary = unicode(unicode(L("search_description"))),
        thumb=R('nrk-nett-tv.png'),
        prompt = unicode(unicode(L("search_title")))))
    
    oc.add(DirectoryObject(
        key = Callback(RecommendedMenu),
        title=unicode(L('recommended_title')), 
        summary=unicode(L('recommended_description')), 
        thumb=R('nrk-nett-tv.png')))

    oc.add(DirectoryObject(
        key = Callback(PopularCategories),
        title=unicode(L('popular_title')), 
        summary=unicode(L('popular_description')), 
        thumb=R('nrk-nett-tv.png')))

    oc.add(DirectoryObject(
        key = Callback(RecentMenu),
        title=unicode(L('recent_title')), 
        summary=unicode(L('recent_description')), 
        thumb=R('nrk-nett-tv.png')))

    oc.add(DirectoryObject(
        key = Callback(CategoriesMenu),
        title=unicode(L('categories_title')), 
        summary=unicode(L('categories_description')), 
        thumb=R('nrk-nett-tv.png')))

    oc.add(PrefsObject(
            title=unicode(L("prefs_title")),
            tagline=unicode(L("prefs_title")),
            summary=unicode(L("prefs_description")),
            thumb=R(ICON_DEFAULT)))

    oc.add(DirectoryObject(
            key = Callback(AboutMenu),
            title=unicode(L("about_title")),
            summary=unicode(L("about_description")),
            thumb=R(ICON_DEFAULT)))

    return oc

def ValidatePrefs():
    return MessageContainer(
        unicode(L("prefs_success_title")),
        unicode(L("prefs_success_description")))