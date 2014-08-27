import sys
import xbmc
import xbmcgui
import xbmcvfs
import xbmcplugin
import xbmcaddon
import StorageServer

settings = xbmcaddon.Addon()
language = settings.getLocalizedString
plugin = settings.getAddonInfo('id')

dbg = settings.getSetting('debug') == 'true'
if dbg:
    dbglevel = 5
else:
    dbglevel = 0


if __name__ == '__main__':
    import CommonFunctions as common
    common.plugin = plugin

    cache = StorageServer.StorageServer(common.plugin,
        int(settings.getSetting('cache_time')))

    common.log('ARGV: ' + repr(sys.argv))

    from resources.lib.utils import Utils
    utils = Utils()

    from resources.lib.api import Api
    api = Api()

    from resources.lib.navigation import Navigation
    navigation = Navigation()

    params = common.getParameters(sys.argv[2])
    if params.get('path'):
        navigation.list_menu(params)
    elif params.get('fetch_login'):
        api.login.login()
    else:
        xbmc.executebuiltin('XBMC.RunScript("%s","%d", "%s")' % (
            plugin, int(sys.argv[1]), '?fetch_login=true'))
        navigation.list_menu()
