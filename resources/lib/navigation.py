import sys


class Navigation(object):
    def __init__(self):
        self.xbmc = sys.modules['__main__'].xbmc
        self.xbmcgui = sys.modules['__main__'].xbmcgui
        self.xbmcplugin = sys.modules['__main__'].xbmcplugin

        self.common = sys.modules['__main__'].common
        self.settings = sys.modules['__main__'].settings
        self.utils = sys.modules['__main__'].utils
        self.cache = sys.modules['__main__'].cache
        self.api = sys.modules['__main__'].api

        _ = self.utils.get_string

        self.categories = (
            {'Title': _('shows'),       'path': '/root/shows',          'folder': 'true', 'get': 'shows'},
            {'Title': _('search'),      'path': '/root/search',         'folder': 'true', 'get': 'search'},
            {'Title': _('episodes'),    'path': '/root/shows/episodes', 'folder': 'true', 'type': 'episodes'},
            {'Title': _('movies'),      'path': '/root/shows/movies',   'folder': 'true', 'type': 'movies'},
            {'Title': _('trailers'),    'path': '/root/shows/trailers', 'folder': 'true', 'type': 'trailers'},
            {'Title': _('clips'),       'path': '/root/shows/clips',    'folder': 'true', 'type': 'clips'},
        )

    def list_menu(self, params=None):
        self.common.log(repr(params), 5)
        if params is None:
            params = {}

        get = params.get
        path = get('path', '/root')
        if (get('get') not in ['search', 'shows'] or get('show')) and not get('type'):
            for category in self.categories:
                cat_get = category.get
                if cat_get('path').find(path + '/') > -1:
                    if cat_get('path').rfind('/') <= len(path + '/'):
                        if cat_get('type') == 'episodes' and not get('has_episodes'):
                            continue
                        if cat_get('type') == 'movies' and not get('has_movies'):
                            continue
                        if cat_get('type') == 'trailers' and not get('has_trailers'):
                            continue
                        if cat_get('type') == 'clips' and not get('has_clips'):
                            continue
                        self.add_list_item(params, category)

        if get('get') in ['shows', 'search'] or get('show') or get('store') or get('type'):
            if get('type') or get('get') in ['shows', 'search']:
                return self.list(params)

        video_view = self.settings.getSetting('list_view') == '1'
        if video_view:
            self.xbmc.executebuiltin('Container.SetViewMode(500)')

        self.xbmcplugin.endOfDirectory(handle=int(sys.argv[1]), succeeded=True)
        self.common.log('Done', 5)

    def list(self, params=None):
        self.common.log(repr(params), 5)
        if params is None:
            params = {}

        get = params.get
        if get('get') == 'search':
            if not get('search'):
                query = self.common.getUserInput(self.utils.get_string('search'), '')
                if not query:
                    return False
                self.parse_show_list(params, self.api.search_shows(query))
                self.common.log('Done', 5)
                return True
        elif get('get') == 'shows':
            results = self.api.get_shows()
            if results:
                self.parse_show_list(params, results)
                self.common.log('Done', 5)
                return True
            else:
                params['error'] = 'Failed to get shows'
                self.show_listing_error(params)
                self.common.log('Error')
                return False
        elif get('show'):
            if get('type') == 'episodes':
                results = self.api.get_episodes(get('show'), get('page', 0))
                if results:
                    self.parse_episode_list(params, results)
                    self.common.log('Done', 5)
                    return True
                else:
                    params['error'] = 'Show has no episodes'
                    self.show_listing_error(params)
                    self.common.log('Error')
                    return False
            elif get('type') == 'movies':
                results = self.api.get_movies(get('show'), get('page', 0))
                if results:
                    self.parse_movie_list(params, results)
                    self.common.log('Done', 5)
                    return True
                else:
                    ret_params = {'path': '/root/shows', 'show': get('show')}
                    params['error'] = 'Show has no movies'
                    self.show_listing_error(params)
                    self.common.log('Error')
                    return ret_params
            elif get('type') == 'trailers':
                results = self.api.get_trailers(get('show'), get('page', 0))
                if results:
                    self.parse_trailers_list(params, results)
                    self.common.log('Done', 5)
                    return True
                else:
                    params['error'] = 'Show has no trailers'
                    self.show_listing_error(params)
                    self.common.log('Error')
                    return False
            elif get('type') == 'clips':
                results = self.api.get_clips(get('show'), get('page', 0))
                if results:
                    self.parse_clips_list(params, results)
                    self.common.log('Done', 5)
                    return True
                else:
                    params['error'] = 'Show has no clips'
                    self.show_listing_error(params)
                    self.common.log('Error')
                    return False

    def show_listing_error(self, params=None):
        self.common.log(repr(params), 5)
        if params is None:
            params = {}
        self.utils.show_error_message(params['error'])

    def add_list_item(self, params=None, item_params=None):
        self.common.log('params: %s items: %s' % (repr(params), repr(item_params)), 5)
        if item_params is None:
            item_params = {}
        if params is None:
            params = {}

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
        self.common.log('params: %s items: %s' % (repr(params), repr(item_params)), 5)
        if item_params is None:
            item_params = {}
        if params is None:
            params = {}

        get = params.get
        item = item_params.get

        if get('show') and item('type'):
            item_params['show'] = get('show')
            item_params['type'] = item('type')
            if get('has_episodes'):
                item_params['episodes'] = 'true'
            if get('has_movies'):
                item_params['movies'] = 'true'
            if get('has_trailers'):
                item_params['trailers'] = 'true'
            if get('has_clips'):
                item_params['clips'] = 'true'

        icon = 'DefaultFolder.png'
        if item('icon'):
            icon = self.utils.get_thumbnail(item('icon'))

        thumbnail = item('thumbnail')

        if item('thumbnail', 'DefaultFolder.png').find('http://') == -1:
            thumbnail = self.utils.get_thumbnail(item('thumbnail'))

        list_item = self.xbmcgui.ListItem(item('Title'), iconImage=icon, thumbnailImage=thumbnail)
        # list_item.setInfo('video', get('info'))

        url = '%s?path=%s&' % (sys.argv[0], item('path'))
        url = self.utils.build_item_url(item_params, url)

        list_item.setProperty('Folder', 'true')

        self.xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=list_item, isFolder=True, totalItems=size)
        self.common.log('Done', 9)

    def add_action_list_item(self, params=None, item_params=None, size=0):
        self.common.log('params: %s items: %s' % (repr(params), repr(item_params)), 5)
        if params is None:
            params = {}
        if item_params is None:
            item_params = {}

        folder = True
        item = item_params.get
        icon = 'DefaultFolder.png'
        thumbnail = self.utils.get_thumbnail(item('thumbnail'))
        list_item = self.xbmcgui.ListItem(item('Title'), iconImage=icon, thumbnailImage=thumbnail)

        url = '%s?path=%s&' % (sys.argv[0], item("path"))
        url += 'action=' + item("action") + '&'

        self.xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=list_item, isFolder=folder, totalItems=size)
        self.common.log('Done', 5)

    def add_video_list_item(self, params=None, item_params=None, size=0):
        self.common.log('params: %s items: %s' % (repr(params), repr(item_params)), 9)
        if item_params is None:
            item_params = {}
        if params is None:
            params = {}

        item = item_params.get
        url = self.utils.stream_url(item('videoid'), item('hd'))
        icon = self.utils.get_thumbnail(item('icon', 'default'))
        list_item = self.xbmcgui.ListItem(item('Title'), iconImage=icon, thumbnailImage=item('thumbnail'))

        list_item.setProperty('Is_playable', 'true')
        list_item.setInfo('video', item('info'))

        self.xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=list_item, isFolder=False, totalItems=size + 1)
        self.common.log('Done', 9)

    def add_folder_context_menu_items(self, params=None, item_params=None):
        self.common.log('params: %s items: %s' % (repr(params), repr(item_params)), 5)
        if item_params is None:
            item_params = {}
        if params is None:
            params = {}
        self.common.log('Done', 5)

    def add_video_context_menu_items(self, params=None, item_params=None):
        self.common.log('params: %s items: %s' % (repr(params), repr(item_params)), 5)
        if params is None:
            params = {}
        if item_params is None:
            item_params = {}
        self.common.log('Done', 5)

    def execute_action(self, params=None):
        self.common.log(repr(params), 5)
        if params is None:
            params = {}
        get = params.get
        if get('action') == 'play_video':
            self.common.log('playing video: %s' % get('videoid'))

        self.common.log('Done', 5)

    def parse_show_list(self, params, results):
        self.common.log(repr(params), 5)
        list_size = len(results)
        for show in results.all(params.get('type')):
            self.add_folder_list_item(params, show, list_size)

        self.xbmcplugin.endOfDirectory(handle=int(sys.argv[1]))
        self.common.log('Done', 5)

    def parse_episode_list(self, params, results):
        self.common.log(repr(params), 5)
        list_size = len(results)
        item = {'path': '/root/shows/episodes', 'folder': 'true', 'show': results.show_id, 'type': 'episodes'}
        for episode in results.itemize():
            self.add_video_list_item(params, episode, list_size)

        if results.has_more():
            item['Title'] = 'Next >>'
            item['page'] = str(int(results.page) + 1)
            item['thumbnail'] = 'next'
            self.add_folder_list_item(params, item)

        video_view = int(self.settings.getSetting("list_view")) >= 1
        if video_view:
            self.xbmc.executebuiltin("Container.SetViewMode(500)")

        self.xbmcplugin.endOfDirectory(handle=int(sys.argv[1]))
        self.common.log('Done', 5)

    def parse_movie_list(self, params, results):
        self.common.log(repr(params), 5)
        list_size = len(results.movies)
        item = {'path': '/root/shows/movies', 'folder': 'true', 'show': results.show_id, 'type': 'movies'}
        for movie in results.itemize():
            self.add_video_list_item(params, movie, list_size)

        if results.has_more():
            item['Title'] = 'Next >>'
            item['page'] = str(int(results.page) + 1)
            item['thumbnail'] = 'next'
            self.add_folder_list_item(params, item)

        video_view = int(self.settings.getSetting("list_view")) >= 1
        if video_view:
            self.xbmc.executebuiltin("Container.SetViewMode(500)")

        self.xbmcplugin.endOfDirectory(handle=int(sys.argv[1]))
        self.common.log('Done', 5)

    def parse_trailers_list(self, params, results):
        self.common.log(repr(params), 5)
        list_size = len(results)
        item = {'path': '/root/shows/trailers', 'folder': 'true', 'show': results.show_id, 'type': 'trailers'}
        for trailer in results.itemize():
            self.add_video_list_item(params, trailer, list_size)

        if results.has_more():
            item['Title'] = 'Next >>'
            item['page'] = str(int(results.page) + 1)
            item['thumbnail'] = 'next'
            self.add_folder_list_item(params, item)

        video_view = int(self.settings.getSetting("list_view")) >= 1
        if video_view:
            self.xbmc.executebuiltin("Container.SetViewMode(500)")

        self.xbmcplugin.endOfDirectory(handle=int(sys.argv[1]))
        self.common.log('Done', 5)

    def parse_clips_list(self, params, results):
        self.common.log(repr(params), 5)
        list_size = len(results)
        item = {'path': '/root/shows/clips', 'folder': 'true', 'show': results.show_id, 'type': 'clips'}
        for clip in results.itemize():
            self.add_video_list_item(params, clip, list_size)

        if results.has_more():
            item['Title'] = 'Next >>'
            item['page'] = str(int(results.page) + 1)
            item['thumbnail'] = 'next'
            self.add_folder_list_item(params, item)

        video_view = int(self.settings.getSetting("list_view")) >= 1
        if video_view:
            self.xbmc.executebuiltin("Container.SetViewMode(500)")

        self.xbmcplugin.endOfDirectory(handle=int(sys.argv[1]), succeeded=True, cacheToDisc=True)
        self.common.log('Done', 5)
