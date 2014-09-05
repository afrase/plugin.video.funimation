from sys import modules, argv
from .core import Core
from .login import Login


order_types = ['asc', 'desc']
rating_type = ['tvpg', 'tv14', 'tvma', 'nr', 'pg', 'pg13', 'r', 'all']
sort_types = ['alpha', 'date', 'dvd', 'now', 'soon', 'votes', 'episode',
              'title', 'sequence']
genre_types = ['all', 'action', 'adventure', 'bishonen', 'bishoujo', 'comedy',
               'cyberpunk', 'drama', 'fan service', 'fantasy', 'harem',
               'historical', 'horror', 'live action', 'magical girl',
               'martial arts', 'mecha', 'moe', 'mystery', 'reverse harem',
               'romance', 'school', 'sci fi', 'shonen', 'slice of life',
               'space', 'sports', 'super power', 'supernatural', 'yuri']

urls = {
    'details':  'mobile/node/{showid}.json',
    'search':   'mobile/shows.json/alpha/asc/nl/all/all?keys={term}',
    'shows':    'mobile/shows.json/{sort}/{order}/{limit}/{rating}/{genre}',
    'clips':    'mobile/clips.json/sequence/{order}/{showid}/all/all?page={page}',
    'trailers': 'mobile/trailers.json/sequence/{order}/{showid}/all/all?page={page}',
    'movies':   'mobile/movies.json/{v_type}/{sort}/{order}/all/{showid}?page={page}',
    'episodes': 'mobile/episodes.json/{v_type}/sequence/{order}/all/{showid}?page={page}',
    'stream':   '{base_url}/038C48/SV/480/{video_id}/{video_id}-480-{quality}K.mp4.m3u8?{uid}',
}


class Api(Core):

    def __init__(self):
        super(Api, self).__init__()
        self.login = Login()
        self.cache = modules['__main__'].cache
        self.xbmcplugin = modules['__main__'].xbmcplugin

    def get_data(self, method, params):
        params = self._check_params(**params)
        url = urls[method].format(**params)
        return self._get_data(url)

    def get_search(self, term, **kwargs):
        self.log('Searching for: ' + term, 4)
        url = urls['search'].format(**locals())
        return self._get_data(url)

    def get_shows(self, **kwargs):
        kwargs = self._check_params(**kwargs)

        self.xbmcplugin.setContent(int(argv[1]), 'tvshows')
        url = urls['shows'].format(**kwargs)
        return self._get_data(url)

    def get_episodes(self, **kwargs):
        kwargs = self._check_params(**kwargs)

        self.xbmcplugin.setContent(int(argv[1]), 'episodes')
        url = urls['episodes'].format(**kwargs)
        return self._get_data(url)

    def get_movies(self, **kwargs):
        kwargs = self._check_params(**kwargs)

        self.xbmcplugin.setContent(int(argv[1]), 'movies')
        url = urls['movies'].format(**kwargs)
        return self._get_data(url)

    def get_trailers(self, **kwargs):
        kwargs = self._check_params(**kwargs)

        self.xbmcplugin.setContent(int(argv[1]), 'episodes')
        url = urls['trailers'].format(**kwargs)
        return self._get_data(url)

    def get_clips(self, **kwargs):
        kwargs = self._check_params(**kwargs)

        self.xbmcplugin.setContent(int(argv[1]), 'episodes')
        url = urls['clips'].format(**kwargs)
        return self._get_data(url)

    def get_details(self, **kwargs):
        kwargs = self._check_params(**kwargs)
        url = urls['details'].format(**kwargs)
        return self._get_data(url)

    def stream_url(self, video_id, hd=False):
        # TODO: figure out the max quality
        if hd:
            quality = '3500'
        else:
            quality = '2000'

        base_url = 'http://wpc.8c48.edgecastcdn.net'
        # this value doesn't seem to change
        uid = '9b303b6c62204a9dcb5ce5f5c607'
        url = urls['stream'].format(**locals())
        self.log(url, 5)
        return url

    def _get_data(self, url):
        resp = self.get(url)
        try:
            return self.common.process_response(resp)
        except Exception, e:
            self.log(e, 4)
            return []

    def _check_params(self, showid=0, page=0, sort=None, order=None, limit=None, rating=None, genre=None, term=None, **kwargs):
        if sort is None or sort_types not in sort:
            sort = 'alpha'

        if order is None or order_types not in order:
            order = 'asc'

        if limit is None or not limit.isdigit():
            limit = 'nl'  # no limit

        if rating is None or rating not in rating_type:
            rating = 'all'

        if genre is None or genre not in genre_types:
            genre = 'all'

        if term is None:
            term = ''

        # this is can be streaming but not sure how to tell what to use yet.
        # maybe if logged in it's subscription if not it's streaming?
        if self.login.logged_in:
            v_type = 'subscription'
        else:
            v_type = 'streaming'

        return locals()
