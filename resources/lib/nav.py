import os
from sys import modules, argv

xbmcplugin = modules['__main__'].xbmcplugin
xbmcgui = modules['__main__'].xbmcgui
common = modules['__main__'].common
api = modules['__main__'].api
handle = int(argv[1])

# this list should be in a central spot
genre_types = ['action', 'adventure', 'bishonen', 'bishoujo', 'comedy',
               'cyberpunk', 'drama', 'fan_service', 'fantasy', 'harem',
               'historical', 'horror', 'live_action', 'magical_girl',
               'martial_arts', 'mecha', 'moe', 'mystery', 'reverse_harem',
               'romance', 'school', 'sci_fi', 'shonen', 'slice_of_life',
               'space', 'sports', 'super_power', 'supernatural', 'yuri']

_ = common.get_string

# static menu items
menus = (
    {'label': _('shows'),      'path': '/show',            'folder': 'true', 'get': 'shows'},
    {'label': _('genres'),     'path': '/genre',           'folder': 'true'},
    {'label': _('search'),     'path': '/search',          'folder': 'true'},
    {'label': _('episodes'),   'path': '/show/episodes',   'folder': 'true', 'get': 'episodes'},
    {'label': _('movies'),     'path': '/show/movies',     'folder': 'true', 'get': 'movies'},
    {'label': _('clips'),      'path': '/show/clips',      'folder': 'true', 'get': 'clips'},
    {'label': _('trailers'),   'path': '/show/trailers',   'folder': 'true', 'get': 'trailers'},
)

def list_menu():
    params = common.get_params()
    common.log('PARAMS: ' + repr(params))
    get = params.get('get')
    path = params.get('path', '/')
    # if query has get then it should run something
    if get:
        get_menu_data(params)
    elif path == '/genre':
        display_grenres()
    elif path == '/search':
        display_search()
    else:
        for menu in menus:
            m_path = os.path.dirname(menu['path'])
            # if path in query is parent of static menu path
            if m_path == path:
                vtypes = params.get('vtypes')
                # a show selection will have vtypes param which is a CSV of the
                # supposid video types for that show.
                if vtypes:
                    # only create menu items for what the show has.
                    if menu.get('get') in vtypes.split(','):
                        # we need to keep the show ID past the video type
                        # selection to pass to whatever type is selected
                        menu['showid'] = params.get('id')
                        add_list_item(menu)
                else:
                    # query doesn't have vtypes then it's top menu
                    add_list_item(menu)

    xbmcplugin.endOfDirectory(handle)


def display_grenres():
    for genre in genre_types:
        q = {'label': _(genre), 'path': '/genre', 'folder': 'true',
             'get': 'shows', 'genre': genre.replace('_', ' ')}
        add_list_item(q)


def display_search():
    term = common.get_user_input(_('search_shows'))
    params = {'get': 'search', 'term': term}
    get_menu_data(params)


def add_list_item(query, items=None):
    if items is None:
        items = query

    if query.get('folder'):
        add_folder_list_item(query, items)
    elif query.get('videoid'):
        add_video_list_item(query, items)

def get_list_item(items):
    get = items.get
    li = xbmcgui.ListItem(get('label'), get('label2'), get('icon'), get('thumbnail'))
    li.setInfo('video', get('info'))
    return li

def add_folder_list_item(query, items):
    url = common.build_url(query)
    common.log(url, 5)
    li = get_list_item(items)
    xbmcplugin.addDirectoryItem(handle, url, li, True, items.get('total', 0))

def add_video_list_item(query, items):
    url = api.stream_url(query.get('videoid'), items.hd)
    li = get_list_item(items)
    common.log(url, 5)
    li.setProperty('Is_playable', 'true')
    xbmcplugin.addDirectoryItem(handle, url, li, False, items.get('total', 0))

def get_menu_data(params):
    get = params['get']
    resp = api.get_data(get, params)

    total_items = len(resp)
    common.log('Got %d %s' % (total_items, get), 4)
    if total_items == 50:
        add_next_item(params)

    if total_items == 0:
        display_error_item(params)

    for item in resp:
        item.total = total_items
        add_list_item(item.query_string, item)

def display_error_item(params):
    query = {}
    # no_episodes, no_movies, etc.
    query['label'] = _('no_' + params.get('get'))
    query['folder'] = 'true'
    query['showid'] = params.get('showid')
    add_list_item(query)

def add_next_item(params):
    query = {}
    query['label'] = _('next') + ' >>'
    query['path'] = '/show/next'
    query['folder'] = 'true'
    query['get'] = params.get('get')
    query['page'] = int(params.get('page', 0)) + 1
    query['showid'] = params.get('showid')
    add_list_item(query)
