# -*- coding: utf-8 -*-
import sys
#reload(sys)
#sys.setdefaultencoding("utf-8")
import os, datetime, xbmcplugin, xbmcgui, xbmc, xbmcaddon
import simplejson as json
#extra imports
from resources.lib.functions import *
from resources.lib.rlocas import *

appdata = xbmc.validatePath(xbmc.translatePath(xbmcaddon.Addon('plugin.audio.songza').getAddonInfo('profile')))
if not os.path.isdir(appdata):
    os.makedirs(appdata)
#Day and Day-Period dictionaries
day_name = {0: "Sunday", 1: "Monday", 2: "Tuesday", 3: "Wednesday",
            4: "Thursday", 5: "Friday", 6: "Saturday",}
period_name = {0: "Morning", 1: "Late Morning", 2: "Afternoon",
            3: "Evening", 4: "Night", 5: "Late Night",} 

#Calculate Songza Day and Period 
tdelta = datetime.timedelta
now = datetime.datetime.now()
day_start = datetime.datetime(now.year,now.month,now.day)
sz_day = 0 if now.isoweekday()==7 else now.isoweekday()

if now < (day_start+tdelta(hours=4)):
    sz_day = 6 if sz_day==0 else sz_day-1
    sz_period = 5
    next
elif now < (day_start+tdelta(hours=8)):
    sz_period = 0
    next
elif now < (day_start+tdelta(hours=12)):
    sz_period = 1
    next
elif now < (day_start+tdelta(hours=16)):
    sz_period = 2
    next
elif now < (day_start+tdelta(hours=20)):
    sz_period = 3
    next
else:
    sz_period = 4

#Debug
#print "The day is "+str(sz_day)+" and the period is "+str(sz_period)
#print "Which is called "+day_name[sz_day]+" "+period_name[sz_period]
#print day_start.isoformat()
#print now.isoformat()

#Menu Generation test
#for (day_id, day_title) in day_name.items():
#    for (period_id, period_title) in period_name.items():
#        selected = "(Current)" if day_id == sz_day and period_id == sz_period else ""
#        print day_title, period_title, selected
mode=None
params=get_params()
try:
        mode=str(params['mode'])
except:
        pass

if mode==None:
    add_dir('Concierge ({0!s} {1!s})'.format(day_name[sz_day],period_name[sz_period]),'?mode=situations&sz_day='+str(sz_day)+'&sz_period='+str(sz_period))
    add_dir('Choose another time','?mode=day')
    add_dir('Popular','?mode=popular')
    add_dir('Browse All','?mode=browse')
    
if mode=='day':
    for (day_id, day_title) in day_name.items():
        add_dir(day_title,'?mode=period&sz_day='+str(day_id))

if mode=='period':
    for (period_id, period_title) in period_name.items():
        sz_day=str(params['sz_day'])
        add_dir(period_title,'?mode=situations&sz_day='+sz_day+'&sz_period='+str(period_id))

if mode=='popular':
    r = OpenUrl('http://songza.com/api/1/chart/name/songza/all-time')
    r = json.loads(r)
    for item in r:
        #xbmc.log(item);
        add_dir(item['name'],'?mode=subpop&sz_popid='+str(item['id']))
        #f = open(os.path.join(appdata,item['id']), 'w+')
        #f.write(str(item['situations']))
        #f.close()

if mode=='browse':
    r = OpenUrl('http://songza.com/api/1/tags')
    r = json.loads(r)
    for item in r:
        add_dir(item['name'],'?mode=subbrowse&sz_browseid='+item['id'])

if mode=='subbrowse':
    sz_browseid=str(params['sz_browseid'])
    r = OpenUrl('http://songza.com/api/1/gallery/tag/'+sz_browseid)
    r = json.loads(r)
    for item in r:
        add_dir(item['name'],'?mode=subbrowse&sz_browseid='+item['id'])


if mode=='situations':
    sz_day=str(params['sz_day'])
    sz_period=str(params['sz_period'])
    r = OpenUrl('http://songza.com/api/1/situation/targeted?device=web&site=songza&current_date='+str(now.isoformat())+'&day='+sz_day+'&period='+sz_period)
    r = json.loads(r)
    for item in r:
        add_dir(item['title'],'?mode=situation&sz_situation='+item['id'])
        f = open(os.path.join(appdata,item['id']), 'w+')
        f.write(str(item['situations']))
        f.close()

#if mode=='situation':
    
xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=False)
