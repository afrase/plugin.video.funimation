from .base_controller import BaseController
from resources.lib.models.clip import Clip


class ClipsController(BaseController):

    def __init__(self, node, show_id=None, page='0'):
        super(ClipsController, self).__init__()
        self.show_id = show_id
        self.page = int(page)
        self.json = node

        if isinstance(self.json, dict):
            get = self.json.get
            if get('node') > 0:
                for attr in get('node'):
                    self.log(attr, 9)
                    self._items.append(Clip(attr['show']))

    def itemize(self):
        return [ep.itemize() for ep in self]
