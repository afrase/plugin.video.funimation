import os
from sys import modules, argv
from .models import Show

xbmcplugin = modules['__main__'].xbmcplugin
xbmcgui = modules['__main__'].xbmcgui
xbmc = modules['__main__'].xbmc
common = modules['__main__'].common
api = modules['__main__'].api
handle = int(argv[1])

_ = common.get_string

# static menu items
menus = (
    {'label': _('shows'), 'path': '/show', 'folder': 'true', 'get': 'shows'},
    {'label': 'Browse Latest', 'path': '/show', 'folder': 'true', 'get': 'latest'},
    {'label': 'Browse Simulcasts', 'path': '/show', 'folder': 'true', 'get': 'simulcast'},
)

def list_menu():
    params = common.get_params()
    get_param = params.get('get')
    path = params.get('path', '/')

    # if query has get then it should run something
    if get_param:
        generate_menu(params)
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

    if handle > -1:
        xbmcplugin.endOfDirectory(handle)


def display_grenres():

        q = {'label': _(genre), 'path': '/genre', 'folder': 'true',
             'get': 'shows', 'genre': genre}
        add_list_item(q)


def display_search():
    term = common.get_user_input(_('search_shows'))
    params = {'get': 'search', 'term': term}
    generate_menu(params)


def add_list_item(query, item=None):
    if item is None:
        item = query

    if query.get('folder'):
        add_folder_list_item(query, item)
    elif query.get('videoid'):
        add_video_list_item(query, item)


def add_folder_list_item(query, item):
    common.log('query: %s item: %s' % (repr(query), repr(item)), common.DEBUG)
    url = common.build_url(query)
    li = gen_list_item(item)
    xbmcplugin.addDirectoryItem(handle, url, li, True, item.get('total', 0))


def add_video_list_item(query, item):
    common.log('query: %s item: %s' % (repr(query), repr(item)), common.DEBUG)
    url = item.get('video_url')
    li = gen_list_item(item)
    li.setProperty('Is_playable', 'true')
    li.addStreamInfo('video', item.stream_info)
    xbmcplugin.addDirectoryItem(handle, url, li, False, item.get('total', 0))


def gen_list_item(item):
    get = item.get
    li = xbmcgui.ListItem(get('label'), get('label2'), get('icon'), get('thumbnail'))
    if get('info'):
        li.setInfo('video', get('info'))
    return li


def generate_menu(query):
    get = query['get']

    if get == 'episodes':
        xbmcplugin.setContent(handle, 'episodes')
    elif get == 'movies':
        xbmcplugin.setContent(handle, 'movies')
    elif get == 'shows':
        xbmcplugin.setContent(handle, 'tvshows')

    resp = api.get_data(get, query)

    if get == 'details':
        return display_details(query, resp)

    total_items = len(resp)
    common.log('Got %d %s' % (total_items, get), common.INFO)

    if total_items == 0:
        display_error_item(query)

    for item in resp:
        item.total = total_items
        add_list_item(item.query_string, item)

    # since there is no way to know if there are more items from a query
    # we just assume if we get the max for the query there might be more
    if get in ('episodes','movies','clips','trailers'):
        # if we are filtering video types then divide the max
        max_item = 50 if common.sub_dub == 0 else 25
        if total_items >= max_item:
            add_more_item(query)


def display_details(query, item):
    # TODO: figure out a way to update show details after list item is
    #       already displayed if possible
    xbmc.executebuiltin('XBMC.Action(Info)')


def display_error_item(query):
    common.log('No items returned for query', common.WARN)
    # no_episodes, no_movies, etc.
    query['label'] = _('no_results')
    query['folder'] = 'true'
    query['showid'] = query.get('showid')
    add_list_item(query)


def add_more_item(query):
    get = query.get
    query['label'] = _('more')
    query['path'] = '/show/more'
    query['folder'] = 'true'
    query['get'] = get('get')
    query['page'] = int(get('page', 0)) + 1
    query['showid'] = get('showid')
    add_list_item(query)
