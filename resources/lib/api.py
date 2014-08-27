from sys import modules

from .controllers.clips_controller import ClipsController
from .controllers.episodes_controller import EpisodesController
from .controllers.movies_controller import MoviesController
from .controllers.shows_controller import ShowsController
from .controllers.trailers_controller import TrailersController
from .controllers.user_controller import UserController
from .core import Core
from .login import Login


class Api(Core):

    def __init__(self):
        super(Api, self).__init__()

        self.login = Login()
        self.cache = modules['__main__'].cache

        self.sort_types = ['alpha', 'date', 'dvd', 'now', 'soon', 'votes', 'episode', 'title', 'sequence']
        self.order_types = ['asc', 'desc']
        self.rating_type = ['tvpg', 'tv14', 'tvma', 'nr', 'pg', 'pg13', 'r', 'all']
        self.genre_types = ['all', 'action', 'adventure', 'bishonen', 'bishoujo', 'comedy', 'cyberpunk', 'drama',
                            'fan_service', 'fantasy', 'harem', 'historical', 'horror', 'live_action', 'magical_girl',
                            'martial_arts', 'mecha', 'moe', 'mystery', 'reverse_harem', 'romance', 'school', 'scifi',
                            'shonen', 'slice_of_life', 'space', 'sports', 'super_power', 'supernatural', 'yuri']

        self.urls = {
            'shows': '/mobile/shows.json/{sort}/{order}/{limit}/{rating}/{genre}',
            'episodes': '/mobile/episodes.json/{v_type}/{sort}/{order}/all/{show_id}?page={page}',
            'movies': '/mobile/movies.json/{v_type}/{sort}/{order}/all/{show_id}?page={page}',
            'trailers': '/mobile/trailers.json/{sort}/{order}/{show_id}/all/all?page={page}',
            'clips': '/mobile/clips.json/{sort}/{order}/{show_id}/all/all?page={page}',
            'search': '/mobile/shows.json/alpha/asc/nl/all/all?keys={term}'
        }

    def search_shows(self, term):
        self.log(term, 5)
        url = self.urls['search'].format(**locals())

        response = self.http.get(url)
        self.log('Done', 5)
        try:
            return ShowsController(response)
        except Exception, e:
            self.log(e)
            return None

    def get_shows(self, sort=None, order=None, limit=None, rating=None, genre=None):
        self.log(locals(), 5)
        if sort is None or self.sort_types not in sort:
            sort = 'alpha'

        if order is None or self.order_types not in order:
            order = 'asc'

        if limit is None or not limit.isdigit():
            limit = 'nl' # no limit

        if rating is None or self.rating_type not in rating:
            rating = 'all'

        if genre is None or self.genre_types not in genre:
            genre = 'all'

        url = self.urls['shows'].format(**locals())
        response = self.cache.cacheFunction(self.get, url)
        try:
            return ShowsController(response)
        except Exception, e:
            self.log(e)
            return None

    def get_episodes(self, show_id, page=0, sort=None, order=None):
        self.log(locals(), 5)
        if sort is None or self.sort_types not in sort:
            sort = 'sequence'

        if order is None or self.order_types not in order:
            order = 'asc'

        # this is can be streaming but not sure how to tell what to use yet.
        # maybe if logged in it's subscription if not it's streaming?
        v_type = 'subscription'

        url = self.urls['episodes'].format(**locals())
        response = self.cache.cacheFunction(self.get, url)

        try:
            return EpisodesController(response, show_id, page)
        except Exception, e:
            self.log(e)
            return None

    def get_movies(self, show_id, page=0, sort=None, order=None):
        self.log(locals(), 5)
        if sort is None or self.sort_types not in sort:
            sort = 'sequence'

        if order is None or self.order_types not in order:
            order = 'asc'

        v_type = 'subscription'

        url = self.urls['movies'].format(**locals())
        response = self.cache.cacheFunction(self.get, url)
        try:
            return MoviesController(response, show_id, page)
        except Exception, e:
            self.log(e)
            return None

    def get_trailers(self, show_id, page=0, sort=None, order=None):
        self.log(locals(), 5)
        if sort is None or self.sort_types not in sort:
            sort = 'sequence'

        if order is None or self.order_types not in order:
            order = 'asc'

        url = self.urls['trailers'].format(**locals())
        self.log(url)
        response = self.cache.cacheFunction(self.get, url)
        try:
            return TrailersController(response, show_id, page)
        except Exception, e:
            self.log(e)
            return None

    def get_clips(self, show_id, page=0, sort=None, order=None):
        self.log(locals(), 5)
        if sort is None or self.sort_types not in sort:
            sort = 'sequence'

        if order is None or self.order_types not in order:
            order = 'asc'

        url = self.urls['clips'].format(**locals())
        self.log(url)
        response = self.cache.cacheFunction(self.get, url)
        try:
            return ClipsController(response, show_id, page)
        except Exception, e:
            self.log(e)
            return None
