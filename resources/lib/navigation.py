import sys
from resources.lib.api import Api


class Navigation(object):
    def __init__(self):
        self.xbmc = sys.modules['__main__'].xbmc
        self.xbmcgui = sys.modules['__main__'].xbmcgui
        self.xbmcplugin = sys.modules['__main__'].xbmcplugin

        self.common = sys.modules['__main__'].common
        self.plugin = sys.modules['__main__'].plugin
        self.utils = sys.modules['__main__'].utils
        self.api = Api()

        _ = self.utils.get_string

        self.categories = (
            {'Title': _('shows'),       'path': '/root/shows',              'thumbnail': 'shows',       'folder': 'true', 'get': 'shows'},
            {'Title': _('search'),      'path': '/root/search',             'thumbnail': 'search',      'folder': 'true', 'get': 'search'},
            {'Title': _('episodes'),    'path': '/root/shows/episodes',     'thumbnail': 'shows',       'folder': 'true', 'type': 'episodes'},
            {'Title': _('movies'),      'path': '/root/shows/movies',       'thumbnail': 'movies',      'folder': 'true', 'type': 'movies'},
            {'Title': _('trailers'),    'path': '/root/shows/trailers',     'thumbnail': 'trailers',    'folder': 'true', 'type': 'trailers'},
            {'Title': _('clips'),       'path': '/root/shows/clips',        'thumbnail': 'featured',    'folder': 'true', 'type': 'clips'},
        )

    def list_menu(self, params=None):
        self.common.log(repr(params), 5)
        if not params: params = {}

        get = params.get
        cache = True

        path = get('path', '/root')
        if (get('get') not in ['search', 'shows'] or get('show')) and not get('type'):
            for category in self.categories:
                cat_get = category.get
                if cat_get('path').find(path + '/') > -1:
                    if cat_get('path').rfind('/') <= len(path + '/'):
                        self.add_list_item(params, category)

        if get('get') in ['shows', 'search'] or get('show') or get('store') or get('type'):
            if get('type') or get('get') in ['shows', 'search']:
                return self.list(params)

        video_view = self.plugin.getSetting('list_view') == '1'
        if video_view:
            self.xbmc.executebuiltin('Container.SetViewMode(500)')

        self.xbmcplugin.endOfDirectory(handle=int(sys.argv[1]), succeeded=True, cacheToDisc=cache)
        self.common.log('Done', 5)

    def list(self, params=None):
        self.common.log(repr(params), 5)
        if not params: params = {}

        get = params.get
        if get('get') == 'search':
            if not get('search'):
                query = self.common.getUserInput(self.utils.get_string('search'), '')
                if not query:
                    return False
                params['search'] = query
        elif get('get') == 'shows':
            results, status = self.api.get_shows()
            if status == 200:
                self.parse_show_list(params, results)
                self.common.log('Done', 5)
                return True
            else:
                self.show_listing_error(params)
                self.common.log('Error')
                return False
        # show must be defined
        elif get('show'):
            if get('type') == 'episodes':
                results, status = self.api.get_episodes(get('show'), get('page', 0))
                if status == 200:
                    self.parse_episode_list(params, results)
                    self.common.log('Done', 5)
                    return True
                else:
                    self.show_listing_error(params)
                    self.common.log('Error')
                    return False
            elif get('type') == 'movies':
                results, status = self.api.get_movies(get('show'), get('page', 0))
                if status == 200:
                    self.parse_movie_list(params, results)
                    self.common.log('Done', 5)
                    return True
                else:
                    self.show_listing_error(params)
                    self.common.log('Error')
                    return False
            elif get('type') == 'trailers' or get('type') == 'clips':
                self.utils.show_message('Funimation', 'Not yet implemented')

    def show_listing_error(self, params=None):
        self.common.log(repr(params), 5)
        if not params: params = {}
        pass

    def add_list_item(self, params=None, item_params=None):
        self.common.log(repr(item_params), 5)
        if not item_params: item_params = {}
        if not params: params = {}

        item = item_params.get

        if not item('action'):
            if item('login', 'false') == 'false':
                self.add_folder_list_item(params, item_params)
        else:
            if item('action') == 'play_video':
                self.add_video_list_item(params, item_params)
            else:
                self.add_folder_list_item(params, item_params)

        self.common.log('Done', 5)

    def add_folder_list_item(self, params=None, item_params=None, size=0):
        self.common.log('params: %s items: %s' % (repr(params), repr(item_params)), 9)
        if not item_params: item_params = {}
        if not params: params = {}

        get = params.get
        item = item_params.get

        if get('show') and item('type'):
            item_params['show'] = get('show')
            item_params['type'] = item('type')

        icon = 'DefaultFolder.png'
        if item('icon'):
            icon = self.utils.get_thumbnail(item('icon'))

        thumbnail = item('thumbnail')

        if item('thumbnail', 'DefaultFolder.png').find('http://') == -1:
            thumbnail = self.utils.get_thumbnail(item('thumbnail'))

        list_item = self.xbmcgui.ListItem(item('Title'), iconImage=icon, thumbnailImage=thumbnail)
        url = '%s?path=%s&' % (sys.argv[0], item('path'))
        url = self.utils.build_item_url(item_params, url)

        list_item.setProperty('Folder', 'true')

        self.xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=list_item, isFolder=True, totalItems=size)
        self.common.log('Done', 9)

    def add_action_list_item(self, params=None, item_params=None, size=0):
        self.common.log('', 5)
        if not params: params = {}
        if not item_params: item_params = {}

        item = item_params.get
        folder = True
        icon = 'DefaultFolder.png'
        thumbnail = self.utils.get_thumbnail(item('thumbnail'))
        list_item = self.xbmcgui.ListItem(item('Title'), iconImage=icon, thumbnailImage=thumbnail)

        url = '%s?path=%s&' % (sys.argv[0], item("path"))
        url += 'action=' + item("action") + '&'

        self.xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=list_item, isFolder=folder,
                                         totalItems=size)
        self.common.log('Done', 5)

    def add_video_list_item(self, params=None, item_params=None, size=0):
        self.common.log('params: %s items: %s' % (repr(params), repr(item_params)), 9)
        if not item_params: item_params = {}
        if not params: params = {}
        item = item_params.get
        get = params.get
        get('icon')
        icon = item('icon', 'default')

        icon = self.utils.get_thumbnail(icon)
        list_item = self.xbmcgui.ListItem(item('Title'), iconImage=icon, thumbnailImage=item('thumbnail'))
        # url = '%s?path=%s&action=play_video&videoid=%s' % (sys.argv[0], '/root/video', item('videoid'))
        url = self.utils.stream_url(item('videoid'))

        list_item.setProperty('Video', 'true')
        list_item.setProperty('IsPlayable', 'true')
        list_item.setInfo(type='Video', infoLabels=item_params['info'])

        self.xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=list_item, isFolder=False, totalItems=size + 1)
        self.common.log('Done', 9)

    def add_folder_context_menu_items(self, params=None, item_params=None):
        self.common.log('', 5)
        if not item_params: item_params = {}
        if not params: params = {}
        self.common.log('Done', 5)

    def add_video_context_menu_items(self, params=None, item_params=None):
        self.common.log('', 5)
        if not params: params = {}
        if not item_params: item_params = {}
        self.common.log('Done', 5)

    def execute_action(self, params=None):
        self.common.log(repr(params), 5)
        if not params: params = {}
        get = params.get
        if get('action') == 'play_video':
            self.common.log('playing video: %s' % get('videoid'))

        self.common.log('Done', 5)

    def parse_show_list(self, params, results):
        self.common.log(repr(params), 9)
        list_size = len(results.shows)
        for show in results.all(params.get('type')):
            self.add_folder_list_item(params, show, list_size)

        self.xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=self.xbmcplugin.SORT_METHOD_UNSORTED)
        self.xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=self.xbmcplugin.SORT_METHOD_LABEL)
        self.xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=self.xbmcplugin.SORT_METHOD_VIDEO_RATING)
        self.xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=self.xbmcplugin.SORT_METHOD_DATE)
        self.xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=self.xbmcplugin.SORT_METHOD_PROGRAM_COUNT)
        self.xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=self.xbmcplugin.SORT_METHOD_VIDEO_RUNTIME)
        self.xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=self.xbmcplugin.SORT_METHOD_GENRE)

        self.xbmcplugin.endOfDirectory(handle=int(sys.argv[1]), succeeded=True, cacheToDisc=True)
        self.common.log('Done', 9)

    def parse_episode_list(self, params, results):
        self.common.log(repr(params), 9)
        list_size = len(results.episodes)
        item = {'path': '/root/shows/episodes', 'folder': 'true', 'show': results.show_id, 'type': 'episodes'}
        for episode in results.itemize():
            self.add_video_list_item(params, episode, list_size)

        if results.has_more():
            item['Title'] = 'Next >>'
            item['page'] = str(int(results.page) + 1)
            item['thumbnail'] = 'next'
            self.add_folder_list_item(params, item)

        video_view = int(self.plugin.getSetting("list_view")) >= 1
        if video_view:
            self.xbmc.executebuiltin("Container.SetViewMode(500)")

        self.xbmcplugin.endOfDirectory(handle=int(sys.argv[1]), succeeded=True, cacheToDisc=True)
        self.common.log('Done', 9)

    def parse_movie_list(self, params, results):
        self.common.log(repr(params), 9)
        list_size = len(results.movies)
        item = {'path': '/root/shows/movies', 'folder': 'true', 'show': results.show_id, 'type': 'movies'}
        for movie in results.itemize():
            self.add_video_list_item(params, movie, list_size)

        if results.has_more():
            item['Title'] = 'Next >>'
            item['page'] = str(int(results.page) + 1)
            item['thumbnail'] = 'next'
            self.add_folder_list_item(params, item)

        video_view = int(self.plugin.getSetting("list_view")) >= 1
        if video_view:
            self.xbmc.executebuiltin("Container.SetViewMode(500)")

        self.xbmcplugin.endOfDirectory(handle=int(sys.argv[1]), succeeded=True, cacheToDisc=True)
        self.common.log('Done', 9)