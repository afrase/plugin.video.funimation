from resources.lib.controllers.base_controller import BaseController
from resources.lib.models.show import Show


class ShowsController(BaseController):
    def __init__(self, node):
        super(ShowsController, self).__init__()

        self.json = node

        if isinstance(self.json, dict):
            if len(self.json['videos']) > 0:
                for attr in self.json['videos']:
                    self._common.log(attr, 9)
                    self._items.append(Show(attr['video']))

        # blacklist shows that have nothing to watch
        self.show_blacklist = ['51579', '51580', '469', '51581', '51807', '51557', '1', '5']

    def all(self, s_type):
        return [i.itemize(s_type) for i in self._items if self.allowed_genres(i.genres) and i.nid not in self.show_blacklist]

    def with_movies(self):
        return [i.itemize() for i in self._items if i.has_movies()]

    def with_trailers(self):
        return [i.itemize() for i in self._items if i.has_trailers()]

    def with_clips(self):
        return [i.itemize() for i in self._items if i.has_clips()]

    def allowed_genres(self, show_genres):
        for genre in show_genres:
            if self._plugin.getSetting(genre) == 'false':
                self._common.log('%s not allowed' % genre, 9)
                return False
        return True