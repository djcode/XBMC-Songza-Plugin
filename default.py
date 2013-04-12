import sys, datetime, xbmcplugin, xbmcgui
#extra imports
from resources.lib.functions import *

#Day and Day-Period dictionaries
day_name = {0: "Sunday", 1: "Monday", 2: "Tuesday", 3: "Wednesday",
            4: "Thursday", 5: "Friday", 6: "Saturday",}
period_name = {0: "Morning", 1: "Late Morning", 2: "Afternoon",
            3: "Evening", 4: "Night", 5: "Late Night",} 

#Calculate Songza Day and Period 
tdelta = datetime.timedelta
now = datetime.datetime.now()
day_start = datetime.datetime(now.year,now.month,now.day)
sz_day = now.isoweekday()

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
    listitem = xbmcgui.ListItem(day_name[sz_day]+" "+period_name[sz_period])
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), sys.argv[0]+'?mode=situation', listitem)
    listitem = xbmcgui.ListItem('Choose another time')
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), sys.argv[0]+'?mode=dayperiod', listitem, isFolder=True)

if mode=='dayperiod':
    for (day_id, day_title) in day_name.items():
        for (period_id, period_title) in period_name.items():
            listitem = xbmcgui.ListItem(day_title+" "+period_title)
            if not xbmcplugin.addDirectoryItem(int(sys.argv[1]), '', listitem): break
xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=False)
