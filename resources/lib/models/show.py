from resources.lib.models import base_model


class Show(base_model.BaseModel):
    def __init__(self, json):
        super(Show, self).__init__(json)
        self.maturity = json['maturity rating']
        self.post_date = json['post date']
        self.genres = json['all terms'].split(', ')
        self.votes = json['votes']
        self.mobile_banner_large = json['mobile_banner_large']
        self.similar_shows = json['similar_shows'].split(',')
        self.video_section = json['Video section']

    def has_episodes(self):
        return self.__has_video_type__('Episodes')

    def has_movies(self):
        return self.__has_video_type__('Movies')

    def has_clips(self):
        return self.__has_video_type__('Clips')

    def has_trailers(self):
        return self.__has_video_type__('Trailers')

    def itemize(self):
        return {
            'label': self.title,
            'icon': self.show_thumbnail,
            'thumbnail': self.mobile_banner_large,
            'path': self.plugin.url_for('episodes_list', show_id=self.nid)
        }

    def __has_video_type__(self, v_type):
        if isinstance(self.video_section, dict):
            for i in self.video_section.items():
                if i[1] == v_type:
                    return True
        return False
