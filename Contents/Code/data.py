# -*- coding: utf-8 -*-

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
import httplib, urllib

PROGRAM_URL = Regex('\/program\/([^\/]+)')
PROGRAM_IMAGE_BASE_URL = 'http://nrk.eu01.aws.af.cm/f/%s'
PROGRAM_LETTER_BASE_URL = BASE_URL + '/programmer/%s'
JSON_URL_RECENT = BASE_URL + '/listobjects/recentlysent.json/page/0/100'
JSON_URL_POPULAR_WEEK = BASE_URL + '/listobjects/mostpopular/Week.json/page/0/100'
JSON_URL_POPULAR_MONTH = BASE_URL + '/listobjects/mostpopular/Month.json/page/0/100'
JSON_URL_CATEGORY = BASE_URL + '/listobjects/indexelements/%s/page/0'

def GetRecommended():
    start_page = HTML.ElementFromURL(BASE_URL)

    items = start_page.xpath("//*[@id='recommended-list']/ul/li/div/a")
    titles = []
    urls = []
    thumbs = []
    fanarts = []
    summaries = []
    for item in items:
        urls.append(BASE_URL + item.get('href'))
        titles.append(item.xpath('./div/img')[0].get('alt'))
        #Log("NRK - title: " + item.xpath('./div/img')[0].get('alt'))
        thumbs.append(item.xpath('./div/img')[0].get('src'))
        fanarts.append(FanartURL(item.get('href')))
        summaries.append('')

    return titles, urls, thumbs, fanarts, summaries

def GetByLetter(letterUrl):
    Log.Debug("Letter: " + letterUrl)
    return ProgramList(PROGRAM_LETTER_BASE_URL % letterUrl)

def GetMostRecent():
    return JSONList(JSON_URL_RECENT)

def GetMostPopularWeek():
    return JSONList(JSON_URL_POPULAR_WEEK)

def GetMostPopularMonth():
    return JSONList(JSON_URL_POPULAR_MONTH)

def GetSeasons(url):
    #NOT WORKING!
    #returns: </program/Episodes/aktuelt-tv/11998> """
    Log.Debug("URL: " + url)
    html = HTML.ElementFromURL(url)
    noScriptHtml = html.xpath("//*[@id='seasons']/noscript/text()")
    noScriptHtml = HTML.ElementFromString(noScriptHtml)
    Log.Debug(noScriptHtml)
    items = noScriptHtml.xpath("//a")
    Log.Debug("Items: " + str(items))
    titles = []
    urls = []
    thumbs = []
    fanarts = []
    summaries = []
    for item in items:
        titles.append('Sesong ' + item.get('title'))
        urls.append(BASE_URL + item.get('href'))
        fanarts.append(FanartURL(item.get('href')))
        thumbs.append(FanartURL(item.get('href')))
        summaries.append('')
    
    return titles, urls, thumbs, fanarts, summaries
