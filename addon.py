from xbmcswift2 import Plugin

from resources.lib.api import FunimationApi
from resources.lib.utils import Utils


plugin = Plugin()
log = plugin.log.debug
_ = Utils().get_string

ALL = 'all'
EPISODES = 'episodes'
MOVIES = 'movies'
CLIPS = 'clips'
TRAILERS = 'trailers'


def get_api():
    log('Getting API')
    if plugin.get_setting('username') and plugin.get_setting('password'):
        return FunimationApi(
            plugin.get_setting('username'),
            plugin.get_setting('password'))
    else:
        return FunimationApi()


api = get_api()


@plugin.route('/', name='home')
def index():
    items = [
        {'label': _('tv_shows'), 'path': plugin.url_for('show_list', v_type=ALL)},
        {'label': _('episodes'), 'path': plugin.url_for('show_list', v_type=EPISODES)},
        {'label': _('movies'), 'path': plugin.url_for('show_list', v_type=MOVIES)},
        {'label': _('clips'), 'path': plugin.url_for('show_list', v_type=CLIPS)},
        {'label': _('trailers'), 'path': plugin.url_for('show_list', v_type=TRAILERS)},
        {'label': _('search'), 'path': plugin.url_for('show_search')},
        {'label': _('clear_cache'), 'path': plugin.url_for('clear_cache')},
    ]
    return items


@plugin.route('/show_list/<v_type>')
def show_list(v_type=ALL):
    shows = api.get_shows()
    if shows:
        if v_type == EPISODES:
            log('Getting all shows with episodes')
            return plugin.finish(shows.with_episodes())
        elif v_type == MOVIES:
            log('Getting all shows with movies')
            return plugin.finish(shows.with_movies())
        elif v_type == CLIPS:
            log('Getting all shows with clips')
            return plugin.finish(shows.with_clips())
        elif v_type == TRAILERS:
            log('Getting all shows with trailers')
            return plugin.finish(shows.with_trailers())
        elif v_type == ALL:
            log('Getting all shows')
            return plugin.finish(shows.all())
    else:
        plugin.notify(_('show_list_error'))
        plugin.finish(index())


@plugin.route('/episodes_list/<show_id>')
def episodes_list(show_id):
    episodes = api.get_episodes(show_id)
    if episodes:
        return plugin.finish(episodes.itemize())
    else:
        plugin.notify('No episodes for this show')
        return plugin.finish(show_list(EPISODES))


@plugin.route('/show_search')
def show_search():
    term = plugin.keyboard()
    shows = api.search_shows(term)
    return plugin.finish(shows.all())


@plugin.route('/play_video/<video_id>')
def play_video(video_id):
    plugin.set_resolved_url(stream_url(video_id))


@plugin.route('/clear_cache')
def clear_cache():
    Utils().clear_cache()
    plugin.notify(_('clear_cache_msg'))
    return plugin.finish(index())


@plugin.cached()
def stream_url(fun_id):
    # TODO: move to base_video
    # TODO: break the url up
    url = 'http://wpc.8c48.edgecastcdn.net/038C48/SV/480/%s/%s-480-2000K.mp4.m3u8?9b303b6c62204a9dcb5ce5f5c607' % (
        fun_id, fun_id)
    Utils().get_log(url)
    return url


if __name__ == '__main__':
    plugin.run()
