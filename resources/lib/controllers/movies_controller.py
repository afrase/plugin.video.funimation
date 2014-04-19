from resources.lib.controllers.base_controller import BaseController
from resources.lib.models.movie import Movie


class MoviesController(BaseController):
    def __init__(self, node, show_id=None, page='0'):
        super(MoviesController, self).__init__()

        self.show_id = show_id
        self.page = int(page)
        self.json = node

        if isinstance(self.json, dict):
            get = self.json.get
            if get('nodes') > 0:
                for attr in get('nodes'):
                    self._common.log(attr, 9)
                    self._items.append(Movie(attr['show']))

    def itemize(self):
        sb = int(self._plugin.getSetting('sub_dub'))
        if sb == 1:
            self._common.log('getting subs', 9)
            return [ep.itemize() for ep in self if ep.sub()]
        elif sb == 2:
            self._common.log('getting subs', 9)
            return [ep.itemize() for ep in self if ep.dub()]
        else:
            self._common.log(sb, 9)
            return [ep.itemize() for ep in self]