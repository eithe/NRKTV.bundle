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

@route(pluginRoute('/search'))
def SearchResults(query):
    oc = ObjectContainer()
    search_page = HTML.ElementFromURL(BASE_URL + "sok?q=" + query + "&filter=rettigheter")

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

    items = start_page.xpath("//ul[@id='introSlider']/li")
    for item in items:
        title = item.xpath(".//article//strong")[0].text
        url = BASE_URL + item.xpath(".//a")[0].get('href')

        image = ICON_DEFAULT
        img_tag = item.xpath(".//img")
        if img_tag:
            image = img_tag[0].get('src')

        
        summary = item.xpath(".//h1//a/text()")[0].strip()
        # [Optional] - The subtitle
        subtitle = None
        try: subtitle = String.StripTags(item.xpath(".//article/strong/text()")[0]) 
        except: pass

        oc.add(EpisodeObject(
            url = url,
            title = title,
            summary = summary, 
            thumb = image))
    return oc

@route(pluginRoute('/recent'))
def RecentMenu():
    oc = ObjectContainer()
    list_page = HTML.ElementFromURL(BASE_URL + '/listobjects/recentlysent')
    items = list_page.xpath("//li[@class='listobject ']")
    for item in items:
        
        title = String.StripTags(item.xpath(".//span[@class='listobject-title']/strong")[0].text)
        url = BASE_URL + item.xpath(".//a")[0].get('href')
        image = item.xpath(".//img")[0].get('src')
        summary = item.xpath(".//div[@class='stack-links']//a/text()")[0].strip()

        oc.add(EpisodeObject(
            url = url,
            title = title,
            summary = summary,
            thumb = image))
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

@route(pluginRoute('/category/{x}'))
def CategoryMenu(url):
    oc = ObjectContainer()
    list_page = HTML.ElementFromURL(url)
    items = list_page.xpath("//div[@class='alpha-list clear']//li//a")
    for item in items:
        title = item.text
        url = BASE_URL + item.get('href')
        if '/program/' in url:
            oc.add(VideoClipObject(
                url = url,
                title = title))
        else:
            oc.add(DirectoryObject(
            key = Callback(SeriesMenu, url = url),
            title = title))
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
            title = item.xpath(".//a")[0].text
            url = item.xpath(".//a")[0].get('href')
            summary = String.StripTags(item.xpath("td[@class='col-time hidden-phone']")[0].text.strip() + " " + item.xpath(".//time")[0].text.strip())

        oc.add(VideoClipObject(
            url = url,
            title = title,
            summary = summary,
            thumb = image))

    if len(oc) == 0:
         oc.add(emptyItem())
    return oc