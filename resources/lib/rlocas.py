import urllib, urllib2, urlparse, re, xbmc, xbmcgui, xbmcplugin, sys
import simplejson as json

def GetArguments():
    return urlparse.parse_qs((sys.argv[2])[1:])

def ListStations():
    AddStation('Coffee Shop Indie', 425)
    AddStation('Test', 426)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    
def AddStation(name, id):
    url = sys.argv[0] + '?mode=player&station=' + str(id)
    listItem = xbmcgui.ListItem(unicode(name), iconImage = 'DefaultMusicPlaylists.png')
    listItem.setInfo('music', {'title': name})
    return xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = url, listitem = listItem)
    
def PlayStation(station):
    # Get and clear the music playlist
    playlist = xbmc.PlayList(xbmc.PLAYLIST_MUSIC)
    playlist.clear()
    
    # Queue two songs so that there is no delay for next song info when skipping
    QueueNextTrack(playlist, station)
    QueueNextTrack(playlist, station)
    
    # Start playing the playlist
    player = xbmc.Player()
    player.play(playlist)
    
def QueueNextTrack(playlist, station):
    try:
        next = OpenUrl('http://songza.com/api/1/station/' + station + '/next')
        next = json.loads(next)
    except:
        # TODO: Retry?
        return
    
    # Create ListItem from next song info
    listItem = xbmcgui.ListItem(unicode(next['song']['title']), unicode(next['song']['artist']['name']))
    listItem.setInfo('music', {'duration': next['song']['duration'], 'genre': next['song']['genre'], 'album': next['song']['album'], 'artist': next['song']['artist']['name'], 'title': next['song']['title']})
    listItem.setThumbnailImage(next['song']['cover_url'])
    
    # Need to add codec info for XBMC to pick the correct player
    listItem.addStreamInfo('audio', {'codec': 'mp3'})
    
    url = sys.argv[0] + '?mode=player&station=' + str(station) + '&play=' + urllib.quote(next['listen_url'])
    playlist.add(url, listItem)

def PlayTrack(station, url):
    # Tell XBMC which URL to stream the song from
    listItem = xbmcgui.ListItem(path = url)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listItem)
    
    # Queue the next song from the station
    playlist = xbmc.PlayList(xbmc.PLAYLIST_MUSIC)
    if playlist.getposition() > (len(playlist) - 3):
        QueueNextTrack(playlist, station)
    
    
def OpenUrl(url):
    request = urllib2.Request(url)
    request.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20')
    response = urllib2.urlopen(request)
    contents = response.read()
    response.close()
    return contents
    
args = GetArguments()

#if 'play' in args:
#    PlayTrack(args['station'][0], args['play'][0])
#elif 'station' in args:
#    PlayStation(args['station'][0])
#else:
#    ListStations()