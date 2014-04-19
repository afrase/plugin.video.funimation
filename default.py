import sys
import xbmc
import xbmcgui
import xbmcvfs
import xbmcplugin
import xbmcaddon
import StorageServer
import CommonFunctions

from resources.lib.controllers.user_controller import UserController
from resources.lib.navigation import Navigation
from resources.lib.utils import Utils

plugin        = xbmcaddon.Addon()
common        = CommonFunctions
addon_name    = plugin.getAddonInfo('name')
addon_id      = plugin.getAddonInfo('id')
addon_version = plugin.getAddonInfo('version')
addon_path    = plugin.getAddonInfo('path').decode('utf-8')
addon_icon    = plugin.getAddonInfo('icon')
language      = plugin.getLocalizedString

dbg = plugin.getSetting('debug') == 'true'
dbg_level = 5 if dbg else 0

common.plugin   = addon_id
common.dbg      = dbg
common.dbglevel = dbg_level

if __name__ == '__main__':
    cache = StorageServer.StorageServer(addon_name, int(plugin.getSetting('cache_time')))
    if dbg:
        common.log('ARGV: ' + repr(sys.argv))
    else:
        common.log(addon_name)

    utils = Utils()
    user = UserController()
    navigation = Navigation()

    if not sys.argv[2]:
        xbmc.executebuiltin('XBMC.RunScript("%s","%d", "%s")' % (addon_id, int(sys.argv[1]), '?fetch_login=true'))
        navigation.list_menu()
    else:
        params = common.getParameters(sys.argv[2])
        if params.get('action'):
            navigation.execute_action(params)
        elif params.get('path'):
            navigation.list_menu(params)
        elif params.get('fetch_login'):
            user.login()
        else:
            common.log('ARGV Nothing done.. verify params ' + repr(params))