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

LIVE_RADIO_BASEURL = 'http://lyd.nrk.no/nrk_radio_'

LIVE_RADIO_STATIONS = (
    # Channel/image filename, name, description
    ('p1_ostlandssendingen', u'P1', u'Den brede kanalen for folk flest. Norges største radiokanal. Bredt distriktstilbud.'),
    ('p2', u'P2', u'Kulturkanalen med kunst, kultur, nyheter, debatt og samfunnsstoff.'),
    ('p3', u'P3', u'Ungdomskanal med mye pop og rock-musikk, humor og skreddersydde nyheter for de unge.'),
    ('mp3', u'mPetre', u'Musikk for de yngre.'),
    ('klassisk', u'Klassisk', u'Klassisk musikk døgnet rundt'),
    ('alltid_nyheter', u'Alltid Nyheter', u'Hyppige nyhetsoppdateringer - BBC kveld/natt.'),
    ('sami', u'Sámi Radio', u'Tilbud for samisktalende.'),
    ('folkemusikk', u'Folkemusikk', u'Fra NRKs unike folkemusikkarkiv.'),
    ('jazz', u'Jazz', u'Jazz døgnet rundt.'),
    ('sport', u'Sport', u'Levende og arkivsport, engelsk fotball.'),
    ('p3_urort', u'P3 Urørt', u'Musikk.'),
    ('p3_pyro', u'P3 Pyro', u'Musikk.'),
    ('p3_radioresepsjonen', u'P3 Radioresepsjonen', u'Alltid Radioresepsjonen.'),
    ('gull', u'Gull', u'Godbiter fra arkivene.'),
    ('super', u'Super', u'Barnetilbud.'),
    ('p1_ostfold', u'P1 Østfold', u''),
    ('p1_buskerud', u'P1 Buskerud', u''),
    ('p1_sogn_og_fjordane', u'P1 Sogn og Fjordane', u''),
    ('p1_rogaland', u'P1 Rogaland', u''),
    ('p1_finnmark', u'P1 Finnmark', u''),
    ('p1_hedmark_og_oppland', u'P1 Hedmark og Oppland', u''),
    ('p1_hordaland', u'P1 Hordaland', u''),
    ('p1_more_og_romsdal', u'P1 Møre og Romsdal', u''),
    ('p1_nordland', u'P1 Nordland', u''),
    ('p1_telemark', u'P1 Telemark', u''),
    ('p1_troms', u'P1 Troms', u''),
    ('p1_trondelag', u'P1 Trøndelag', u''),
    ('p1_vestfold', u'P1 Vestfold', u''),
    ('p1_sorlandet', u'P1 Sørlandet', u'')
)

@route(pluginRoute('/radio_live'))
def LiveRadioMenu():
    oc = ObjectContainer()
    
    # Adds all the station as track items
    for station in LIVE_RADIO_STATIONS:
        url = '%s%s' % (LIVE_RADIO_BASEURL, station[0])
            
        Log.Debug('NRK: Added stream: %s' % url + ', station: %s' % station[1])
        
        # Thumb file
        if station[0].startswith('nrk-p1'):
            thumb_file = 'nrk-p1.png'
        else:
            thumb_file = station[0] + '.png'
        
        oc.add(TrackObject(
          title = station[1],
          url = url,
          artist=station[2],
          thumb=R('nrk-nettradio.png')
        )) # TODO, add all images for the various channels and then R(thumb_file)
    
    return oc
