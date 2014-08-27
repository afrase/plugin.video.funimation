from .base_controller import BaseController
from resources.lib.models.episode import Episode


class EpisodesController(BaseController):
    def __init__(self, node, show_id=None, page='0'):
        super(EpisodesController, self).__init__()

        self.show_id = show_id
        self.page = int(page)
        self.json = node

        if isinstance(self.json, dict):
            if self.json['nodes'] > 0:
                for attr in self.json['nodes']:
                    self.log(attr, 9)
                    self._items.append(Episode(attr['show']))

    def itemize(self):
        sb = int(self.settings.getSetting('sub_dub'))
        if sb == 1:
            self.log('getting subs', 9)
            return [ep.itemize() for ep in self if ep.sub()]
        elif sb == 2:
            self.log('getting subs', 9)
            return [ep.itemize() for ep in self if ep.dub()]
        else:
            self.log(sb, 9)
            return [ep.itemize() for ep in self]
