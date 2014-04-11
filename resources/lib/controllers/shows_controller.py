from resources.lib.models.show import Show
from resources.lib.utils import Utils


class ShowsController(object):
    def __init__(self, json):
        self.json = json
        self.shows = []
        Utils().get_log('Parsing all shows')
        for attr in json['videos']:
            self.shows.append(Show(attr['video']))
        Utils().get_log('Finished parsing all shows')

    def all(self):
        return [i.itemize() for i in self.shows]

    def with_episodes(self):
        return [i.itemize() for i in self.shows if i.has_episodes()]

    def with_movies(self):
        return [i.itemize() for i in self.shows if i.has_movies()]

    def with_clips(self):
        return [i.itemize() for i in self.shows if i.has_clips()]

    def with_trailers(self):
        return [i.itemize() for i in self.shows if i.has_trailers()]