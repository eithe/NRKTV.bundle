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

LIVE_TV_STATIONS = (
    {
        'title': 'NRK 1', 
        'url': 'http://tv.nrk.no/direkte/nrk1',
        'desc': u'Bredt og variert programtilbud. Norges største tv-kanal.', 
        'img': 'nrk1.png'
    },
    {
        'title': 'NRK 2', 
        'url': 'http://tv.nrk.no/direkte/nrk2',
        'desc': u'Fordypningskanalen. Bakgrunns-, dokumentar og nyhetskanal.', 
        'img': 'nrk2.png'
    }, 
    {
        'title': 'NRK Super / NRK 3', 
        'url': 'http://tv.nrk.no/direkte/nrk3',
        'desc': u'Den tredje kanalen tilbyr vekselsvis et barnetilbud og et tilbud for unge voksne med serier, humor film.', 
        'img': 'nrk3.png'
    }
)

@route(pluginRoute('/live'))
def LiveTVMenu():
    oc = ObjectContainer()

    for station in LIVE_TV_STATIONS:
        url = station['url']
        oc.add(VideoClipObject(url = url, title=station['title'], summary=station['desc'], thumb=R(station['img']))) 
    return oc