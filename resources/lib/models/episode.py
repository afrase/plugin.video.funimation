from .base_video import BaseVideo


class Episode(BaseVideo):

    def __init__(self, json):
        super(Episode, self).__init__(json)
        get = self.json.get
        if get('episode number'):
            self.episode_number = get('episode number').split('.')[0]
        else:
            self.episode_number = ''
        self.episode_thumbnail = get('episode thumbnail')
        self.language = get('language')
        self.sub_dub = get('sub-dub')
        self.quality = get('video quality')
        self.hd = False
        if isinstance(self.quality, dict):
            for i in self.quality.items():
                if 'HD' in i[1]:
                    self.hd = True

    def itemize(self):
        return {
            'Title': '%s. %s (%s)' % (self.episode_number, self.title, self.sub_dub),
            'icon': self.show_thumbnail,
            'thumbnail': self.episode_thumbnail,
            'info': {
                'Duration': self.duration,
                'episode': self.episode_number,
                'votes': self.votes,
                'mpaa': self.rating,
            },
            'videoid': self.funimation_id,
            'hd': self.hd
        }
