from .base_video import BaseModel


class Show(BaseModel):

    def __init__(self, json):
        super(Show, self).__init__(json)
        get = self.json.get

        self.maturity = get('maturity rating')
        self.post_date = get('post date')
        self.genres = [i.lower().replace(' ', '_')
                       for i in get('all terms', '').split(', ')]
        self.votes = get('votes')
        self.mobile_banner_large = get('mobile_banner_large')
        self.similar_shows = get('similar_shows', '').split(',')
        self.video_section = get('Video section')

    def has_episodes(self):
        return self._has_video_type('Episodes')

    def has_movies(self):
        return self._has_video_type('Movies')

    def has_clips(self):
        return self._has_video_type('Clips')

    def has_trailers(self):
        return self._has_video_type('Trailers')

    def itemize(self, video_type=None):
        item = {
            'Title': self.title,
            'icon': self.show_thumbnail,
            'thumbnail': self.mobile_banner_large,
            'path': '/root/shows',
            'show': self.nid,
        }
        if video_type:
            item['type'] = video_type
        if self.has_episodes():
            item['has_episodes'] = 'true'
        if self.has_movies():
            item['has_movies'] = 'true'
        if self.has_clips():
            item['has_clips'] = 'true'
        if self.has_trailers():
            item['has_trailers'] = 'true'
        return item

    def _has_video_type(self, v_type):
        if isinstance(self.video_section, dict):
            for i in self.video_section.items():
                if i[1] == v_type:
                    return True
        return False
