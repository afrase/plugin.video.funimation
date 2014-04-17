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
from resources.lib.settings import Settings


plugin        = xbmcaddon.Addon()
common        = CommonFunctions
addon_name    = plugin.getAddonInfo('id')
addon_version = plugin.getAddonInfo('version')
addon_path    = plugin.getAddonInfo('path').decode('utf-8')
addon_icon    = plugin.getAddonInfo('icon')
language      = plugin.getLocalizedString
dbg           = plugin.getSetting('debug') == 'true'
if dbg:
    dbg_level = 10
else:
    dbg_level = 3

common.plugin   = addon_name
common.dbg      = dbg
common.dbglevel = dbg_level

if __name__ == '__main__':
    cache = StorageServer.StorageServer('Funimation')
    if dbg:
        common.log('ARGV: ' + repr(sys.argv))
    else:
        common.log(addon_name)

    settings = Settings()
    utils = Utils()
    user = UserController()
    navigation = Navigation()

    if not sys.argv[2]:
        navigation.list_menu()
    else:
        params = common.getParameters(sys.argv[2])
        if params.get('action'):
            navigation.execute_action(params)
        elif params.get('path'):
            navigation.list_menu(params)
        else:
            common.log('ARGV Nothing done.. verify params ' + repr(params))
