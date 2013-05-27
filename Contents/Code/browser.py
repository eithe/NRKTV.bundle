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

from util import *
import httplib, urllib
   
PROGRAM_URL = Regex('\/program\/([^\/]+)')
PROGRAM_METADATA_BASE_URL = 'http://nrk.no/serum/api/video/%s'
PROGRAM_IMAGE_BASE_URL = 'http://nrk.eu01.aws.af.cm/f/%s'
PROGRAM_LETTER_BASE_URL = 'http://tv.nrk.no/programmer/%s?filter=rettigheter&ajax=true'
JSON_URL_RECENT = 'http://tv.nrk.no/listobjects/recentlysent.json/page'
JSON_URL_POPULAR_WEEK = 'http://tv.nrk.no/listobjects/mostpopular/Week.json/page'
JSON_URL_POPULAR_MONTH = 'http://tv.nrk.no/listobjects/mostpopular/Month.json/page'

@route(pluginRoute('/search'))
def SearchResults(query):
    oc = ObjectContainer()
    search_page = HTML.ElementFromURL(BASE_URL + "/sok?q=" + query + "&filter=rettigheter")

    items = search_page.xpath("//li[@class='listobject ']")
    for item in items:
        title = item.xpath(".//span[@class='listobject-title']/strong")[0].text
        url = item.xpath(".//a")[0].get('href')
        image = item.xpath(".//a/img")[0].get('src')
        summary = item.xpath(".//p/text()")[1].strip()
        # [Optional] - The subtitle
        tagline = None
        try: tagline = String.StripTags(item.xpath(".//div[@class='stack-links']//a/text()")[0]) 
        except: pass

        oc.add(VideoClipObject(
            url = url,
            title = title,
            summary = summary,
            tagline = tagline, 
            thumb = image))
    return oc

@route(pluginRoute('/recommended'))
def RecommendedMenu():
    oc = ObjectContainer()
    start_page = HTML.ElementFromURL(BASE_URL)

    items = start_page.xpath("//*[@id='recommended-list']/ul/li/div")
    for item in items:
        url = BASE_URL + item.xpath(".//a")[0].get('href')
        #Log("NRK - url: " + url)
        oc.add(VideoClipInformation(url))

    return oc

@route(pluginRoute('/popular'))
def PopularCategories():
    oc = ObjectContainer()
    start_page = HTML.ElementFromURL(BASE_URL)
    items = start_page.xpath("//*[@id='tablist-sub']/li")
    for item in items:
        title = item.xpath(".//a")[0].text
        url = item.xpath(".//a")[0].get('href')
        #Log("URL: " + url)
        oc.add(DirectoryObject(
            key = Callback(PopularMenu, url = url),
            title = title,
            summary = unicode(L('category_name') + ': ' + title )))

    if len(oc) == 0:
         oc.add(emptyItem())

    return oc

@route(pluginRoute('/popular/{x}'))
def PopularMenu(url):
    #http://tv.nrk.no/listobjects/mostpopular/Week.json/page
    if 'Week' in url:
        urlJSON = JSON_URL_POPULAR_WEEK
    else:
        urlJSON = JSON_URL_POPULAR_MONTH
    
    #Get paging index
    if '?' in url:
        urlParts = url.split('?')
        baseUrl = urlParts[0]
        strIndex = urlParts[1]
        nextIndex = int(strIndex)+1
    else:
        baseUrl = url
        nextIndex = 0
        
    nextUrl = baseUrl + "?" + str(nextIndex)
    urlJSON = urlJSON + "/" + str(nextIndex)    
    #Log.Debug("NRK - URL: " + url + ", Next URL: " + nextUrl + " , JSON URL: " + urlJSON)
    
    oc = ObjectContainer()
    contentJSON = JSON.ObjectFromURL(urlJSON)
    for item in contentJSON['Data']:
        url = BASE_URL + item['Url']
        oc.add(VideoClipInformation(url))

    oc.add(DirectoryObject(
        key = Callback(PopularMenu, url = nextUrl), 
        title = "Next...", 
        thumb = R('arrow-right.png')))
    
    return oc

@route(pluginRoute('/recent'))
def RecentMenu(url = ''):
    #http://tv.nrk.no/listobjects/recentlysent.json/page
    urlJSON = JSON_URL_RECENT
    if '?' in url:
        urlParts = url.split('?')
        baseUrl = urlParts[0]
        strIndex = urlParts[1]
        nextIndex = int(strIndex)+1
    else:
        baseUrl = url
        nextIndex = 0
        
    nextUrl = baseUrl + "?" + str(nextIndex)
    urlJSON = urlJSON + "/" + str(nextIndex)    

    oc = ObjectContainer()
    contentJSON = JSON.ObjectFromURL(urlJSON)
    for item in contentJSON['Data']:
        url = BASE_URL + item['Url']
        oc.add(VideoClipInformation(url))

    oc.add(DirectoryObject(
        key = Callback(RecentMenu, url = nextUrl), 
        title = "Next...", 
        thumb = R('arrow-right.png')))

        
    return oc

@route(pluginRoute('/categories'))
def CategoriesMenu():
    oc = ObjectContainer()
    list_page = HTML.ElementFromURL(BASE_URL + '/kategori/')
    items = list_page.xpath("//ul[@id='categoryList']//li")
    for item in items:
        title = item.xpath(".//a")[0].text
        url = BASE_URL + item.xpath(".//a")[0].get('href')

        oc.add(DirectoryObject(
            key = Callback(CategoryMenu, url = url),
            title = title,
            summary = unicode(L('category_name') + ': ' + title )))

    if len(oc) == 0:
         oc.add(emptyItem())

    return oc

@route(pluginRoute('/categories/{x}'))
def CategoryMenu(url):
    oc = ObjectContainer()
    list_page = HTML.ElementFromURL(url)
    items = list_page.xpath("//*[@id='programList']/ul/li/a")
    for item in items:
        title = item.text
        url = BASE_URL + item.get('href')
        if '/program/' in url:
            oc.add(VideoClipInformation(url))
        else:
            #http://tv.nrk.no/serie/ekstremsportveko
            seriesName = url.split('/')[4]
            oc.add(DirectoryObject(
            key = Callback(SeriesMenu, url = url),
            title = title,
            thumb = PROGRAM_IMAGE_BASE_URL % seriesName))
    if len(oc) == 0:
         oc.add(emptyItem())
    
    return oc

@route(pluginRoute('/series/{x}'))
def SeriesMenu(url): 
    oc = ObjectContainer()

    list_page = HTML.ElementFromURL(url)
    items = list_page.xpath("//div[@id='lastEpisodes']//table[@class='episodeTable']//tbody//tr[not(contains(@class, 'no-rights'))]")
    image = list_page.xpath("//img[@class='episode-image']")[0].get("src")

    for item in items:
        if( item.xpath(".//time")):
            metaInfoUrl = BASE_URL + item.get("data-tooltipurl")
            url = item.xpath(".//a")[0].get('href')
            oc.add(VideoClipInformation(url))
    
    if len(oc) == 0:
         oc.add(emptyItem())
    return oc

@route(pluginRoute('/letters'))
def LettersMenu():
    #http://tv.nrk.no/programmer/a?filter=rettigheter&ajax=true
    oc = ObjectContainer()

    common = ['0-9'] + map(chr, range(97, 123))
    letters = common + [ u'æ', u'ø', u'å' ]
    letters = [ e.upper() for e in letters ]

    for letter in letters:
        url = PROGRAM_LETTER_BASE_URL % letter
        oc.add(DirectoryObject(
            key = Callback(LetterMenu, url = url),
            title = letter))

    if len(oc) == 0:
         oc.add(emptyItem())
    return oc

@route(pluginRoute('/letters/{x}'))
def LetterMenu(url):
    oc = ObjectContainer()
    list_page = HTML.ElementFromURL(url, cacheTime=0)
    items = list_page.xpath("//*[@id='main']/div/div/div[2]/ul/li/a")
    for item in items:
        title = item.text
        url = BASE_URL + item.get('href')
        if '/program/' in url:
            oc.add(VideoClipInformation(url))
        else:
            #http://tv.nrk.no/serie/ekstremsportveko
            seriesName = url.split('/')[4]
            oc.add(DirectoryObject(
            key = Callback(SeriesMenu, url = url),
            title = title,
            thumb = PROGRAM_IMAGE_BASE_URL % seriesName))
    if len(oc) == 0:
         oc.add(emptyItem())
    
    return oc

def VideoClipInformation(url):
    # Get program metadata from http://nrk.no/serum/api/video/koid20006708
    # Get image from http://nrk.eu01.aws.af.cm/f/al-qaidas-krigere
    urlElements = url.split('/')
    
    if '/program/' in url:
        #http://tv.nrk.no/program/koid37001111/det-nye-afrika
        programId = urlElements[4]
        if len(urlElements) >= 6:
            programName = urlElements[5]
        else:
            programName = ''
    else:
        #http://tv.nrk.no/serie/alf-proeysens-barnesanger/obue14005308/sesong-2/episode-3
        programId = urlElements[5]
        programName = urlElements[4]
        
    metadataURL = PROGRAM_METADATA_BASE_URL % programId
    imageURL = PROGRAM_IMAGE_BASE_URL % programName
    metaJSON = JSON.ObjectFromURL(metadataURL)
    title = metaJSON['title']
    if 'description' in metaJSON:
        summary = metaJSON['description']
    else:
        summary = ''
    image = imageURL
    
    #Log.Debug("NRK: title: " + title + ", Summary: " + summary + ", Image: " + image)

    vc = VideoClipObject(
        url = url,
        title = title,
        summary = summary,
        thumb = image)
    
    return vc