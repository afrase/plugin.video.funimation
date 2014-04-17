from resources.lib.controllers.base_controller import BaseController
from resources.lib.models.show import Show


class ShowsController(BaseController):
    def __init__(self, node):
        super(ShowsController, self).__init__()

        self.json = node
        self.shows = []
        self.common.log('parsing shows', 5)

        if len(self.json['videos']) > 0:
            for attr in self.json['videos']:
                self.shows.append(Show(attr['video']))
            self.common.log('finished parsing shows', 5)

        # blacklist shows that have nothing to watch
        self.show_blacklist = ['51579', '51580', '469', '51581', '51807', '51557', '1', '5']

    def all(self, s_type):
        return [i.itemize(s_type) for i in self.shows if i.nid not in self.show_blacklist and 'Drama' not in i.genres and 'Live Action' not in i.genres]

    def with_movies(self):
        return [i.itemize() for i in self.shows if i.has_movies()]