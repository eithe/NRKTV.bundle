﻿# -*- coding: utf-8 -*-

# "THE BEER-WARE LICENSE" (Revision 42):
# eithe and burnbay @plexforums wrote this file.  As long as you retain this
# notice you can do whatever you want with this stuff. If we meet some day,
# and you think this stuff is worth it, you can buy us a beer in return. Eirik H.

# Some of this stuff is from:
# jonklo's NRK Plex plugin: https://github.com/plexinc-plugins/NRK.bundle
# takoi's NRK XBMC plugin: https://github.com/takoi/xbmc-addon-nrk
# Please comply with their licenses, I haven't looked at them yet.

# NRK, if you are watching, don't hesitate to make contact.

from util import *
from live_radio import LiveRadioMenu
from itertools import repeat
from podcasts import *

####################################################################################################

# Just a small list currently supports SSL HTTP Live Streams
SSL_CAPABLE_CLIENTS = [ClientPlatform.iOS, ClientPlatform.MacOSX]

def Start():
    ObjectContainer.art = R(ART_DEFAULT)
    ObjectContainer.title1 = NAME

    EpisodeObject.art = R(ART_DEFAULT)
    EpisodeObject.thumb = R(ICON_DEFAULT)

    HTTP.CacheTime = CACHE_1HOUR
    #HTTP.Headers['X-Requested-With'] = 'XMLHttpRequest'
    HTTP.Headers['Cookie'] = 'NRK_PLAYER_SETTINGS_TV=devicetype=desktop&preferred-player-odm=hlslink&preferred-player-live=hlslink'

@handler(VIDEO_PREFIX, NAME, thumb=ICON_DEFAULT, art=ART_DEFAULT)
def MainMenu():
    oc = ObjectContainer()
    
    oc.add(DirectoryObject(
        key = Callback(TVMenu),
        title=unicode(L('tv_title')), 
        summary=unicode(L('tv_description')), 
        thumb=R('nrk-nett-tv.png')))
        
    oc.add(DirectoryObject(
        key = Callback(LiveRadioMenu),
        title=unicode(L('live_radio_title')), 
        summary=unicode(L('live_radio_description')), 
        thumb=R('nrk-nettradio.png')))
    
    oc.add(DirectoryObject(
        key = Callback(PodcastMainMenu),
        title=unicode(L('podcasts_title')), 
        summary=unicode(L('podcasts_description')), 
        thumb=R(ICON_DEFAULT)))
    
    return oc

@route(pluginRoute('/tv'))
def TVMenu():
    oc = ObjectContainer()
    
    oc.add(DirectoryObject(
        key = Callback(LiveTVMenu),
        title=unicode(L('livetv_title')), 
        summary=unicode(L('livetv_description')), 
        thumb=R('nrk-nett-tv.png')))

    oc.add(DirectoryObject(
        key = Callback(Recommended),
        title=unicode(L('recommended_title')), 
        summary=unicode(L('recommended_description')), 
        thumb=R('nrk-nett-tv.png')))

    oc.add(DirectoryObject(
        key = Callback(MostRecent),
        title=unicode(L('recent_title')), 
        summary=unicode(L('recent_description')), 
        thumb=R('nrk-nett-tv.png')))

    oc.add(DirectoryObject(
        key = Callback(PopularCategories),
        title=unicode(L('popular_title')), 
        summary=unicode(L('popular_description')), 
        thumb=R('nrk-nett-tv.png')))

    oc.add(DirectoryObject(
        key = Callback(Categories),
        title=unicode(L('categories_title')), 
        summary=unicode(L('categories_description')), 
        thumb=R('nrk-nett-tv.png')))

    oc.add(DirectoryObject(
        key = Callback(Letters),
        title=unicode(L('letters_title')), 
        summary=unicode(L('letters_description')), 
        thumb=R('nrk-nett-tv.png')))
    
    oc.add(SearchDirectoryObject(identifier="com.plexapp.plugins.nrk", title=unicode(L("search_title")), prompt=unicode(L("search_prompt")))) 
    
    return oc

@route(pluginRoute('/live'))
def LiveTVMenu():
    #titles, urls, descs, images = GetLiveStreams()
    oc = ObjectContainer()

    oc.add(VideoClipObject(
        url = 'http://tv.nrk.no/direkte/nrk1', 
        title = 'NRK 1', 
        summary = u'Bredt og variert programtilbud. Norges største tv-kanal.', 
        thumb = R('nrk1.png'))) 
    oc.add(VideoClipObject(
        url = 'http://tv.nrk.no/direkte/nrk2',
        title = 'NRK 2',
        summary = u'Fordypningskanalen. Bakgrunns-, dokumentar og nyhetskanal.',
        thumb = R('nrk2.png')))
    oc.add(VideoClipObject(
        url = 'http://tv.nrk.no/direkte/nrk3',
        title = 'NRK 3',
        summary = u'Den tredje kanalen tilbyr vekselsvis et barnetilbud og et tilbud for unge voksne med serier, humor film.',
        thumb = R('nrk3.png')))
    
    return oc

@route(pluginRoute('/recommended'))
def Recommended():
    import data
    return View(*data.GetRecommended())

@route(pluginRoute('/recent'))
def MostRecent():
    import data
    return View(*data.GetMostRecent())

@route(pluginRoute('/popular'))
def PopularCategories():
    oc = ObjectContainer()
    oc.add(DirectoryObject(
        key = Callback(MostPopularWeek),
        title = unicode(L('popular_title_week')),
        summary = unicode(L('popular_description_week'))))
    oc.add(DirectoryObject(
        key = Callback(MostPopularMonth),
        title = unicode(L('popular_title_month')),
        summary = unicode(L('popular_description_month'))))

    return oc

@route(pluginRoute('/popularweek'))
def MostPopularWeek():
    import data
    return View(*data.GetMostPopularWeek())

@route(pluginRoute('/popularmonth'))
def MostPopularMonth():
    import data
    return View(*data.GetMostPopularMonth())

@route(pluginRoute('/letters'))
def Letters():
    oc = ObjectContainer()

    common = ['0-9'] + map(chr, range(65, 91))
    letters = common + [ u'Æ', u'Ø', u'Å' ]

    for letter in letters:
        if letter == u'Æ':
            url = "AE"
        elif letter == u'Ø':
            url = "OE"
        elif letter == u'Å':
            url = "AA"
        else:
            url = letter
        
        oc.add(DirectoryObject(
            key = Callback(Letter, letterUrl = url, letter = letter),
            title = letter,
            thumb = R('%s.png' % letter)))

    if len(oc) == 0:
         oc.add(emptyItem())
    return oc

@route(pluginRoute('/letter/{letter}'))
def Letter(letterUrl, letter):
    import data
    return View(*data.GetByLetter(letterUrl))
    
@route(pluginRoute('/categories'))
def Categories():
    import data
    return View(*data.GetCategories())

@route(pluginRoute('/category/{category}'))
def Category(url, category, index = 0):
    import data
    url = BASE_URL + url
    splitUrl = url.split("/")
    category = splitUrl[len(splitUrl)-1]
    #Log.Debug("CATEGORY: " + str(category))
    return View(*data.GetByCategory(category, index))

@route(pluginRoute('/series/{seriesName}'))
def Series(url, seriesName): 
    import data
    return View(*data.GetSeasons(url))

@route(pluginRoute('/episodes/{id}'))
def Episodes(url, id): 
    import data
    return View(*data.GetEpisodes(url))

def View(titles, urls, thumbs=repeat(''), fanarts=repeat(''), summaries=repeat(''), index=0, category = ''):
    #Log.Debug("No of Titles: " + str(len(titles)))
    oc = ObjectContainer()
    total = len(titles)
    if total == 0:
        oc.add(emptyItem())
        return oc
        
    for title, url, thumb, fanart, summary in zip(titles, urls, thumbs, fanarts, summaries):
        #Log.Debug("NRK - url: " + url)
        summary = summary() if callable(summary) else summary
        thumb = thumb() if callable(thumb) else thumb
        fanart = fanart() if callable(fanart) else fanart
        
        if '/Episodes/' in url:
            #Log.Debug("Episodes: " + url)
            urlSplit = url.split('/') #/petter-kanin/38617/msui26001511
            id = urlSplit[len(urlSplit)-1]
            #Log.Debug("SeasonPath: " + seasonPath)
            oc.add(DirectoryObject(
            key = Callback(Episodes, url = url, id = id), title = unicode(title), thumb = thumb, art = fanart))
        elif '/program/' in url or RE_PROG_INFO.search(url): #koid24002713 Playable:
            #Log.Debug("Program: " + url)
            oc.add(VideoClipObject(url = url, title = unicode(title), thumb = thumb, art = fanart, summary = summary))
        elif '/programmer/' in url:
            #Log.Debug("Program: " + url)
            cat = url.split('/')[4] #'barn'
            oc.add(DirectoryObject(
            key = Callback(Category, url = url, category = cat, index = index), title = unicode(title), thumb = R('nrk-nett-tv.png'), art = fanart))
        else:
            #Log.Debug("Series: " + url)
            seriesName = url.split('/')[4] #http://tv.nrk.no/serie/albert-aaberg
            oc.add(DirectoryObject(
            key = Callback(Series, url = url, seriesName = seriesName), title = unicode(title), thumb = thumb, art = fanart))
    
    if index > 0: #Add paging object
        oc.add(DirectoryObject(
            key = Callback(Category, url = BASE_URL + '/programmer/%s' % category, category = category, index = index), title = unicode(L("paging_next")), thumb = R('arrow-right.png'), art = fanart))
    
    return oc
    
def ValidatePrefs():
    return ObjectContainer(
        header=unicode(L("prefs_success_title")),
        message=unicode(L("prefs_success_description")))
