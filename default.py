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

if __name__ == '__main__':
    import resources.lib.common as common
    common.log('ARGV: ' + repr(sys.argv), 4)

    cache = StorageServer.StorageServer(common.plugin,
        int(settings.getSetting('cache_time')))

    from resources.lib.api import Api
    api = Api()

    import resources.lib.nav as nav
    nav.list_menu()
