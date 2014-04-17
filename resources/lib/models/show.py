from resources.lib.models.base_video import BaseModel


class Show(BaseModel):
    def __init__(self, json):
        super(Show, self).__init__(json)
        get = self.json.get

        self.maturity = get('maturity rating')
        self.post_date = get('post date')
        self.genres = get('all terms', '').split(', ')
        self.votes = get('votes')
        self.mobile_banner_large = get('mobile_banner_large')
        self.similar_shows = get('similar_shows', '').split(',')
        self.video_section = get('Video section')

    def has_episodes(self):
        return self.__has_video_type__('Episodes')

    def has_movies(self):
        return self.__has_video_type__('Movies')

    def has_clips(self):
        return self.__has_video_type__('Clips')

    def has_trailers(self):
        return self.__has_video_type__('Trailers')

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
        return item

    def __has_video_type__(self, v_type):
        if isinstance(self.video_section, dict):
            for i in self.video_section.items():
                if i[1] == v_type:
                    return True
        return False
