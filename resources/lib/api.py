from resources.lib.controllers.episodes_controller import EpisodesController
from resources.lib.controllers.user_controller import UserController
from resources.lib.http_client import HttpClient
from resources.lib.controllers.shows_controller import ShowsController
from resources.lib.utils import Utils


# TODO: this needs work
class FunimationApi():
    def __init__(self, username=None, password=None):
        self.__req = HttpClient()
        self.util = Utils()
        self.plugin = self.util.get_plugin()
        self.log = self.util.get_log()

        self.shows = None
        self.episodes = None

        UserController(username, password)

    def get_shows(self):
        shows_cache = self.util.get_show_cache()
        if len(shows_cache.items()) <= 0:
            try:
                self.log('Shows not cached, getting shows')
                shows_cache.update(self.__req.get(
                    '/mobile/shows.json/alpha/asc/nl/all/all'
                ).json())
                shows_cache.sync()
            except:
                return None
        return ShowsController(shows_cache)

    def search_shows(self, term):
        try:
            json = self.__req.get(
                '/mobile/shows.json/alpha/asc/nl/all/all', params={'keys': term}
            ).json()
            return ShowsController(json)
        except:
            return None

    def _get_episodes(self, eid, page=0, items=None):
        if not items: items = {'nodes': []}
        try:
            results = self.__req.get(
                '/mobile/episodes.json/subscription/sequence/asc/all/%s/all/all' % eid,
                params={'page': page}
            ).json()
            if len(results) > 0:
                items['nodes'] += results['nodes']
                return self._get_episodes(eid, page + 1, items)
            else:
                return EpisodesController(items)
        except:
            return None

    def get_episodes(self, eid):
        episode_cache = self.util.get_episode_cache(eid)
        if len(episode_cache.items()) <= 0:
            episode_cache.update(self._get_episodes(eid).json)
            episode_cache.sync()
        return EpisodesController(episode_cache)

    def get_trailers(self, tid):
        try:
            return self.__req.get(
                '/mobile/trailers.json/date/desc/%s/all/all' % tid
            ).json()
        except:
            return None

    def get_clips(self, cid):
        try:
            return self.__req.get(
                '/mobile/clips.json/date/desc/%s/all/all' % cid
            ).json()
        except:
            return None

    def get_movies(self, mid):
        try:
            return self.__req.get(
                '/mobile/movies.json/date/desc/%s/all/all' % mid
            ).json()
        except:
            return None