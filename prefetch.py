import sys
import StorageServer
import CommonFunctions
import xbmcaddon
from resources.lib.api import Api
from resources.lib.controllers.user_controller import UserController
from resources.lib.utils import Utils

if __name__ == '__main__':
    plugin        = xbmcaddon.Addon('plugin.video.funimation')
    common        = CommonFunctions
    addon_name    = plugin.getAddonInfo('name')
    addon_id      = plugin.getAddonInfo('id')
    addon_version = plugin.getAddonInfo('version')
    addon_path    = plugin.getAddonInfo('path').decode('utf-8')
    addon_icon    = plugin.getAddonInfo('icon')
    language      = plugin.getLocalizedString
    dbg           = plugin.getSetting('debug') == 'true'
    if dbg:
        dbg_level = 10
    else:
        dbg_level = 3

    common.plugin   = addon_id
    common.dbg      = dbg
    common.dbglevel = dbg_level

    common.log(sys.argv)

    cache = StorageServer.StorageServer(addon_name, int(plugin.getSetting('cache_time')))

    utils = Utils()
    user = UserController()
    api = Api()

    for show in api.get_shows():
        common.log(show.title)
        api.get_episodes(show.nid)
        api.get_clips(show.nid)
        api.get_movies(show.nid)
        api.get_trailers(show.nid)