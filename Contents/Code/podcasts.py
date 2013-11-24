# -*- coding: utf-8 -*-

# Source code: jonklo. https://github.com/plexinc-plugins/NRK.bundle/blob/master/Contents/Code/podcasts.py
# Adapted to Plex v2.1 for NRK TV

from util import *

CACHE_HTML_INTERVAL = 3600 * 5
CACHE_RSS_FEED_INTERVAL = 3600

PODCAST_URL = 'http://www.nrk.no/podkast/'
PODCAST_ITUNES_NAMESPACE = {'itunes': 'http://www.itunes.com/dtds/podcast-1.0.dtd'}

@route(pluginRoute('/podcasts'))
def PodcastMainMenu():
    oc = ObjectContainer()
    
    oc.add(DirectoryObject(
        key = Callback(PodcastAudioMenu),
        title=unicode(L('podcasts_audio_title')), 
        summary=unicode(L('podcasts_audio_description')), 
        thumb=R(ICON_DEFAULT)))

    oc.add(DirectoryObject(
        key = Callback(PodcastVideoMenu),
        title=unicode(L('podcasts_video_title')), 
        summary=unicode(L('podcasts_video_description')), 
        thumb=R(ICON_DEFAULT)))

    return oc

@route(pluginRoute('/podcasts/audio'))
def PodcastAudioMenu():
    return PodcastMenu(kind='audio')

@route(pluginRoute('/podcasts/video'))
def PodcastVideoMenu():
    return PodcastMenu(kind='video')


def PodcastMenu(kind):
    """
    Show all available feeds, either video or audio.
    """
    oc = ObjectContainer()
    
    page = HTML.ElementFromURL(PODCAST_URL, cacheTime=CACHE_HTML_INTERVAL)
    
    podcast_tables = page.xpath('//div[@class="pod"]/table')
    
    if kind == 'video':
        podcast_table = podcast_tables[0]
    
    else:
        podcast_table = podcast_tables[1]
    
    for tbody in podcast_table:
        tr_title = tbody.xpath('./tr[@class="pod-row"]')
        tr_desc = tbody.xpath('./tr[@class="pod-desc"]')
        tr_rss_url = tbody.xpath('./tr[@class="pod-rss-url"]')
        
        if len(tr_title):
            title = tr_title[0].xpath('./th')[0].text
        
        if len(tr_desc):
            description = tr_desc[0].xpath('./td/p')[0].text
        
        if len(tr_rss_url):
            rss_url = tr_rss_url[0].xpath('./td/a')[0].get('href')
            
            # Fetch the image from the RSS file
            feed = XML.ElementFromURL(rss_url, cacheTime=CACHE_RSS_FEED_INTERVAL)
            
            try:
                image = feed.xpath('//itunes:image', namespaces=PODCAST_ITUNES_NAMESPACE)[0].get('href')
            except AttributeError:
                image = None
            
            # Add it to the list
            oc.add(DirectoryObject(key = Callback(PodcastShowMenu, podcastName=title, podcastUrl=rss_url, podcastSubtitle=description, podcastImage=image, kind = kind), title=title, summary=description, thumb=image))
        
    return oc

def PodcastShowMenu(podcastName=None, podcastUrl=None, podcastSubtitle=None, podcastImage=None, kind=None):
    """
    Show all available items for a given podcast.
    """
    oc = ObjectContainer()
    oc.title2 = podcastName
    
    rss = XML.ElementFromURL(podcastUrl, cacheTime=CACHE_RSS_FEED_INTERVAL)
    
    episodes = rss.xpath('//channel/item')
    
    if len(episodes):
        
        for episode in episodes:
            episodeUrl = episode.xpath('./enclosure')[0].get('url')
            episodeTitle = episode.xpath('./title/text()')[0]
            episodeDate = str(episode.xpath('./pubDate/text()')[0])
            episodeDescription = episode.xpath('./description/text()')[0]
            episodeSubtitle = episodeDate
            Log.Debug("NRK: Adding podcast media object:" + episodeUrl)
            #episodeLength = 0
            if kind == 'audio':
              Log.Debug("NRK: Adding audio as TrackObject:" + episodeUrl)
              oc.add(TrackObject(
                url = episodeUrl,
                title = episodeTitle,
                source_title = "NRK",
                artist = episodeDate))
            else:
              Log.Debug("NRK: Adding video as VideoClipObject:" + episodeUrl)
              oc.add(VideoClipObject(
                url = episodeUrl,
                title = episodeTitle,
                source_title = "NRK"))
    else:
       # Display error message
       oc.add(emptyItem())
    
    return oc
