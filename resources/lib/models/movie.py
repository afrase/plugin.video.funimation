from resources.lib.models.base_video import BaseVideo


class Movie(BaseVideo):
    def __init__(self, json):
        super(Movie, self).__init__(json)
        get = self.json.get

        self.rating = get('rating')
        self.promo = get('Promo') == 'Promo'
        self.sub_dub = get('sub-dub')
        self.tv_thumbnail = get('tv_key_art')

    def itemize(self):
        return {
            'Title': '%s (%s)' % (self.title, self.sub_dub),
            'icon': self.show_thumbnail,
            'thumbnail': self.tv_thumbnail,
            'info': {
                'Duration': self.duration,
                'Rating': self.rating,
            },
            'videoid': self.funimation_id,
            'is_playable': True
        }