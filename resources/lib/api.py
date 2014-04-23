import sys
from resources.lib.controllers.clips_controller import ClipsController
from resources.lib.controllers.episodes_controller import EpisodesController
from resources.lib.controllers.movies_controller import MoviesController
from resources.lib.controllers.shows_controller import ShowsController
from resources.lib.controllers.trailers_controller import TrailersController
from resources.lib.controllers.user_controller import UserController
from resources.lib.http_client import HTTPClient


class Api():
    def __init__(self):
        self.http = HTTPClient()
        self.user = UserController()
        self.common = sys.modules['__main__'].common
        self.cache = sys.modules['__main__'].cache

        self.sort_types = ['alpha', 'date', 'dvd', 'now', 'soon', 'votes', 'episode', 'title', 'sequence']
        self.order_types = ['asc', 'desc']
        self.rating_type = ['tvpg', 'tv14', 'tvma', 'nr', 'pg', 'pg13', 'r', 'all']
        self.genre_types = ['all', 'action', 'adventure', 'bishonen', 'bishoujo', 'comedy', 'cyberpunk', 'drama', 'fan_service', 'fantasy', 'harem', 'historical', 'horror', 'live_action', 'magical_girl', 'martial_arts', 'mecha', 'moe', 'mystery', 'reverse_harem', 'romance', 'school', 'scifi', 'shonen', 'slice_of_life', 'space', 'sports', 'super_power', 'supernatural', 'yuri']

        self.urls = {
            'shows': '/mobile/shows.json/%s/%s/nl/%s/%s',
            'episodes': '/mobile/episodes.json/%s/%s/%s/all/%s?page=%s',
            'movies': '/mobile/movies.json/%s/%s/%s/all/%s?page=%s',
            'trailers': '/mobile/trailers.json/%s/%s/%s/all/all?page=%s',
            'clips': '/mobile/clips.json/%s/%s/%s/all/all?page=%s',
            'search': '/mobile/shows.json/alpha/asc/nl/all/all?keys=%s'
        }

    def search_shows(self, term):
        self.common.log('', 5)
        url = self.urls['search'] % term

        response = self.http.get(url)
        self.common.log('Done', 5)
        try:
            return ShowsController(response)
        except Exception, e:
            self.common.log(e)
            return None

    def get_shows(self, sort_by=None, order_by=None, rating=None, genre=None):
        self.common.log('', 5)
        if not sort_by or self.sort_types not in sort_by:
            sort_by = 'alpha'

        if not order_by or self.order_types not in order_by:
            order_by = 'asc'

        if not rating or self.rating_type not in rating:
            rating = 'all'

        if not genre or self.genre_types not in genre:
            genre = 'all'

        url = self.urls['shows'] % (sort_by, order_by, rating, genre)

        self.user.login()

        response = self.cache.cacheFunction(self.http.get, url)

        self.common.log('Done', 5)
        try:
            return ShowsController(response)
        except Exception, e:
            self.common.log(e)
            return None

    def get_episodes(self, show_id, page=0, sort_by=None, order_by=None):
        self.common.log('', 5)
        if not sort_by or self.sort_types not in sort_by:
            sort_by = 'sequence'

        if not order_by or self.order_types not in order_by:
            order_by = 'asc'

        self.user.login()
        if self.user.logged_in:
            video_type = 'subscription'
        else:
            video_type = 'streaming'

        url = self.urls['episodes'] % (video_type, sort_by, order_by, show_id, page)

        response = self.cache.cacheFunction(self.http.get, url)

        try:
            return EpisodesController(response, show_id, page)
        except Exception, e:
            self.common.log(e)
            return None

    def get_movies(self, show_id, page=0, sort_by=None, order_by=None):
        self.common.log('', 5)
        if not sort_by or self.sort_types not in sort_by:
            sort_by = 'sequence'

        if not order_by or self.order_types not in order_by:
            order_by = 'asc'

        self.user.login()
        if self.user.logged_in:
            video_type = 'subscription'
        else:
            video_type = 'streaming'

        url = self.urls['movies'] % (video_type, sort_by, order_by, show_id, page)

        response = self.cache.cacheFunction(self.http.get, url)

        self.common.log('Done', 5)
        try:
            return MoviesController(response, show_id, page)
        except Exception, e:
            self.common.log(e)
            return None

    def get_trailers(self, show_id, page=0, sort_by=None, order_by=None):
        self.common.log('', 5)
        if not sort_by or self.sort_types not in sort_by:
            sort_by = 'date'

        if not order_by or self.order_types not in order_by:
            order_by = 'desc'

        url = self.urls['trailers'] % (sort_by, order_by, show_id, page)

        response = self.cache.cacheFunction(self.http.get, url)
        self.common.log('Done', 5)
        try:
            return TrailersController(response, show_id, page)
        except Exception, e:
            self.common.log(e)
            return None

    def get_clips(self, show_id, page=0, sort_by=None, order_by=None):
        self.common.log('', 5)
        if not sort_by or self.sort_types not in sort_by:
            sort_by = 'date'

        if not order_by or self.order_types not in order_by:
            order_by = 'desc'

        url = self.urls['clips'] % (sort_by, order_by, show_id, page)

        response = self.cache.cacheFunction(self.http.get, url)

        self.common.log('Done', 5)
        try:
            return ClipsController(response, show_id, page)
        except Exception, e:
            self.common.log(e)
            return None