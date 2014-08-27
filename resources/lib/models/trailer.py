from .base_video import BaseVideo


class Trailer(BaseVideo):

    def __init__(self, json):
        super(Trailer, self).__init__(json)
        get = self.json.get
        self.show_thumbnail = get('show thumbnail')
        self.quality = get('video quality')
        self.hd = False
        if isinstance(self.quality, dict):
            for i in self.quality.items():
                if 'HD' in i[1]:
                    self.hd = True

    def itemize(self):
        return {
            'Title': self.title,
            'icon': self.show_thumbnail,
            'thumbnail': self.show_thumbnail,
            'info': {
                'Duration': self.duration,
                'votes': self.votes,
                'mpaa': self.rating,
            },
            'videoid': self.funimation_id,
            'hd': self.hd
        }
