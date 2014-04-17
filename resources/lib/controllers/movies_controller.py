from resources.lib.controllers.base_controller import BaseController
from resources.lib.models.movie import Movie


class MoviesController(BaseController):
    def __init__(self, node, show_id=None, page='0'):
        super(MoviesController, self).__init__()

        self.show_id = show_id
        self.page = int(page)
        self.json = node
        self.movies = []
        if self.json['nodes'] > 0:
            for attr in self.json['nodes']:
                self.common.log(attr, 10)
                self.movies.append(Movie(attr['show']))

    def itemize(self):
        sb = int(self.plugin.getSetting('sub_dub'))
        if sb == 1:
            self.common.log('getting subs')
            return [ep.itemize() for ep in self.movies if ep.sub()]
        elif sb == 2:
            self.common.log('getting subs')
            return [ep.itemize() for ep in self.movies if ep.dub()]
        else:
            self.common.log(sb)
            return [ep.itemize() for ep in self.movies]

    def has_more(self):
        # seems the api only returns 50 episodes at a time
        return len(self.movies) >= 50