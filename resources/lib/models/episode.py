from resources.lib.models import base_video


class Episode(base_video.BaseVideo):
    def __init__(self, json):
        super(Episode, self).__init__(json)
        self.episode_number = json['episode number'].split('.')[0]
        self.episode_thumbnail = json['episode thumbnail']
        self.language = json['language']
        self.rating = json['rating']
        self.sub_dub = json['sub-dub']

    def itemize(self):
        return {
            'label': '%s. %s' % (self.episode_number, self.title),
            'icon': self.show_thumbnail,
            'thumbnail': self.episode_thumbnail,
            'info': {
                'Duration': self.duration
            },
            'path': self.plugin.url_for('play_video', video_id=self.funimation_id),
            'is_playable': True
        }