from xbmcswift2 import Plugin
from resources.lib.api import FunimationApi


plugin = Plugin()

STRINGS = {
    'tv_shows': 30001,
    'episodes': 30002,
    'movies': 30003,
    'trailers': 30004,
    'clips': 30005,
    'search': 30006,
    'clear_cache': 30007,
    'addon_settings': 30100,
    'show_list_error': 30200,
    'clear_cache_msg': 30300,
}


@plugin.route('/')
def index():
    items = [
        {'label': _('tv_shows'), 'path': plugin.url_for('show_list', video_type='Episodes')},
        #{'label': _('movies'), 'path': plugin.url_for('show_list', video_type='Movies')},
        #{'label': _('search'), 'path': plugin.url_for('show_search')},
        {'label': _('clear_cache'), 'path': plugin.url_for('clear_cache')},
    ]
    return items


# list methods


@plugin.cached_route('/show_list/<video_type>')
def show_list(video_type):
    shows = api.get_shows()
    if shows:
        items = [
            {
                'label': s['video']['title'],
                'icon': s['video']['show thumbnail'],
                'thumbnail': s['video']['mobile_banner_large'],
                'path': plugin.url_for('%s_list' % video_type.lower(),
                                       show_id=s['video']['nid']),
            } for s in shows['videos'] if has_types(s['video']['Video section'], video_type)
        ]
        return items
    else:
        plugin.notify(_('show_list_error'))
        return index


@plugin.cached_route('/episodes_list/<show_id>')
def episodes_list(show_id):
    episodes = api.get_episodes(show_id)
    if episodes:
        items = [
            {
                'label': '%s. %s' % (
                    ep['show']['episode number'].split('.')[0],
                    ep['show']['title']),
                'thumbnail': ep['show']['episode thumbnail'],
                'info': {
                    'Duration': ep['show']['duration'].split(':')[0],
                },
                'path': plugin.url_for('watch_episode',
                                       episode_id=ep['show']['Funimation ID']),
                'is_playable': True
            } for ep in episodes['nodes'] if 'English' in ep['show']['language']
        ]
        return items
    else:
        return [{'label': 'No Episodes', 'path': 'None'}]


@plugin.route('/trailers_list/<show_id>')
def trailers_list(show_id):
    trailers = api.get_trailers(show_id)
    if trailers:
        items = [
            {
                'label': trail['show']['title'],
                'thumbnail': trail['show']['show thumbnail'],
                'path': plugin.url_for('watch_trailer',
                                       trailer_id=trail['show'][
                                           'Funimation ID']),
                'is_playable': True
            } for trail in trailers['node']
        ]
        return items
    else:
        return [{'label': 'No Trailers', 'path': 'None'}]


@plugin.route('/clips_list/<show_id>')
def clips_list(show_id):
    clips = api.get_clips(show_id)
    if clips:
        items = [
            {
                'label': clp['show']['title'],
                'thumbnail': clp['show']['show thumbnail'],
                'path': plugin.url_for('watch_clip',
                                       clip_id=clp['show']['nid']),
                'is_playable': True
            } for clp in clips['node']
        ]
        return items
    else:
        return [{'label': 'No Movies', 'path': 'None'}]


@plugin.route('/movies_list/<show_id>')
def movies_list(show_id):
    movies = api.get_movies(show_id)
    if movies:
        items = [
            {
                'label': mov['show']['title'],
                'thumbnail': mov['show']['show thumbnail'],
                'path': plugin.url_for('watch_movie',
                                       movie_id=mov['show']['nid']),
                'is_playable': True
            } for mov in movies['nodes']
        ]
        return items
    else:
        return [{'label': 'No Movies', 'path': 'None'}]


# watch episodes


@plugin.route('/watch_episode/<episode_id>')
def watch_episode(episode_id):
    url = 'http://wpc.8c48.edgecastcdn.net/038C48/SV/480/%s/%s-480-2000K.mp4.m3u8?9b303b6c62204a9dcb5ce5f5c607' % (
        episode_id, episode_id)
    play_video(url)


@plugin.route('/watch_trailer/<trailer_id>')
def watch_trailer(trailer_id):
    pass


@plugin.route('/watch_clip/<clip_id>')
def watch_clip(clip_id):
    pass


@plugin.route('/watch_movie/<movie_id>')
def watch_movie(movie_id):
    pass


@plugin.route('/show_search')
def show_search():
    term = plugin.keyboard()
    shows = api.search_shows(term)
    log(shows)
    return index


@plugin.route('/clear_cache')
def clear_cache():
    plugin.clear_function_cache()
    plugin.notify(_('clear_cache_msg'))


@plugin.route('/play/<url>')
def play_video(url):
    log('Playing url: %s' % url)
    plugin.set_resolved_url(url)


def get_api():
    if plugin.get_setting('username') and plugin.get_setting('password'):
        return FunimationApi(plugin.get_setting('username'),
                             plugin.get_setting('password'))
    else:
        return FunimationApi()


def has_types(param, name):
    if type(param) is dict:
        return name in param.values()
    else:
        return False


def log(text):
    plugin.log.info(text)


def _(string_id):
    if string_id in STRINGS:
        return plugin.get_string(STRINGS[string_id]).encode('utf-8')
    else:
        log('String is missing: %s' % string_id)
        return string_id


api = get_api()

if __name__ == '__main__':
    plugin.run()
