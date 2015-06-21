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

PROGRAM_URL = Regex('\/program\/([^\/]+)')
PROGRAM_LETTER_BASE_URL = BASE_URL + '/programmer/%s'
PROGRAM_CATEGORY_ROOT_URL = BASE_URL + '/programmer/'
PROGRAM_CATEGORY_BASE_URL = BASE_URL + '/programmer/%s'
PROGRAM_CATEGORY_LETTER_BASE_URL = PROGRAM_CATEGORY_BASE_URL + '/%s'
PROGRAM_SEASON_URL = BASE_URL + "/program/Episodes/%s/%s/%s" #"/program/Episodes/schrodingers-katt/22493/dmpv73000114"
JSON_URL_RECENT = BASE_URL + '/listobjects/recentlysent.json/page/0/100'
JSON_URL_RECENT_SENT_BY_CATEGORY = BASE_URL + '/listobjects/recentlysentbycategory/%s.json/page/0'
JSON_URL_POPULAR_WEEK = BASE_URL + '/listobjects/mostpopular/Week.json/page/0/100'
JSON_URL_POPULAR_MONTH = BASE_URL + '/listobjects/mostpopular/Month.json/page/0/100'
JSON_URL_CATEGORY = BASE_URL + '/listobjects/indexelements/%s/page/%s'

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
    #Log.Debug("LETTER URL: " + letterUrl)
    return ProgramList(PROGRAM_LETTER_BASE_URL % letterUrl)

def GetCategories():
    html = HTML.ElementFromURL(PROGRAM_CATEGORY_ROOT_URL)
    categories = html.xpath("//a[@class='hidden-phone']")

    titles = []
    urls = []
    for category in categories:
        titles.append(category.xpath('./text()')[0])
        urls.append(BASE_URL + category.get('href'))

    return titles, urls

def GetByCategory(category, index):
    return JSONList(JSON_URL_CATEGORY % (category, index))

def GetMostRecent():
    return JSONList(JSON_URL_RECENT)

def GetMostPopularWeek():
    return JSONList(JSON_URL_POPULAR_WEEK)

def GetMostPopularMonth():
    return JSONList(JSON_URL_POPULAR_MONTH)

def GetSeasons(url):
    #Log.Debug("GetSeasons URL: " + url)
    html = HTML.ElementFromURL(url)

    programId = html.xpath("/html/head/meta[@name='programid']")
    urlSlashSplit = url.split("/")
    seriesName = urlSlashSplit[len(urlSlashSplit)-1]

    seasons = html.xpath("//a[@class='ga season-link']")
    #Log.Debug("Seasons: " + str(seasons))
    titles = []
    urls = []
    thumbs = []
    fanarts = []
    summaries = []
    for season in seasons:
        titles.append(season.xpath('./text()')[0])
        urls.append(BASE_URL + season.get('href'))
        fanarts.append(FanartURL(url))
        thumbs.append(ThumbURL(url))
        summaries.append('')

    return titles, urls, thumbs, fanarts, summaries

def GetEpisodes(url):
    #Log.Debug("GetEpisodes URL: " + url)
    html = HTML.ElementFromURL(url, headers = {'X-Requested-With':'XMLHttpRequest'})
    episodes = html.xpath("//li[@data-episode] [not(contains(@class, 'no-rights'))]") #//a[not(contains(@id, 'xx'))]
    #Log.Debug("Episodes: " + str(episodes))
    titles = []
    urls = []
    thumbs = []
    fanarts = []
    summaries = []
    for episode in episodes:
        epUrl = BASE_URL + episode.xpath('./a')[0].get('href')
        programInfoObj = GetProgramInfo(epUrl)
        urls.append(epUrl)

        #Log.Debug("OBJECT: " + str(programInfoObj))
        if programInfoObj is not None and programInfoObj['images']['webImages'] is not None:
            titles.append(programInfoObj['fullTitle'])
            thumbs.append(programInfoObj['images']['webImages'][len(programInfoObj['images']['webImages'])-2]['imageUrl'])
            fanarts.append(programInfoObj['images']['webImages'][len(programInfoObj['images']['webImages'])-1]['imageUrl'])
            summaries.append(programInfoObj['description'])
        else:
            titles.append(episode.xpath('./a/div/h3/text()')[0])
            fanarts.append(FanartURL(epUrl.replace(BASE_URL, '')))
            thumbs.append(ThumbURL(epUrl.replace(BASE_URL, '')))
            summaries.append(episode.xpath('./a/div/p[@class="description"]/span/text()')[0])

    return titles, urls, thumbs, fanarts, summaries
