from resources.lib.models.episode import Episode
from resources.lib.utils import Utils


class EpisodesController(object):
    def __init__(self, json):
        self.log = Utils().get_log
        self.json = json
        self.episodes = []
        for attr in json['nodes']:
            self.episodes.append(Episode(attr['show']))

    def itemize(self):
        return [ep.itemize() for ep in self.episodes if ep.dub()]