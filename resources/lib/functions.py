import sys, xbmcgui, xbmcplugin

# Get parameters script from Voinage's tutorial
def get_params():
    param=[]
    paramstring=sys.argv[2]
    if len(paramstring)>=2:
            params=sys.argv[2]
            cleanedparams=params.replace('?','')
            if (params[len(params)-1]=='/'):
                    params=params[0:len(params)-2]
            pairsofparams=cleanedparams.split('&')
            param={}
            for i in range(len(pairsofparams)):
                    splitparams={}
                    splitparams=pairsofparams[i].split('=')
                    if (len(splitparams))==2:
                            param[splitparams[0]]=splitparams[1]
    return param
	
def add_dir(name, url=''):
    li = xbmcgui.ListItem(str(name))
    return xbmcplugin.addDirectoryItem(int(sys.argv[1]), sys.argv[0]+str(url), li, isFolder=True)
    