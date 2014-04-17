from resources.lib.models.base_video import BaseVideo


class Episode(BaseVideo):
    def __init__(self, json):
        super(Episode, self).__init__(json)
        get = self.json.get
        self.episode_number = get('episode number').split('.')[0] if get('episode number') else ''
        self.episode_thumbnail = get('episode thumbnail')
        self.language = get('language')
        self.sub_dub = get('sub-dub')

    def itemize(self):
        return {
            'Title': '%s. %s (%s)' % (self.episode_number, self.title, self.sub_dub),
            'icon': self.show_thumbnail,
            'thumbnail': self.episode_thumbnail,
            'info': {
                'Duration': self.duration
            },
            'videoid': self.funimation_id,
            'is_playable': True
        }

    def _stream_url(self):
        base_url = 'http://wpc.8c48.edgecastcdn.net'
        uid = '9b303b6c62204a9dcb5ce5f5c607'
        url = '%s/038C48/SV/480/%s/%s-480-2000K.mp4.m3u8?%s' % \
              (base_url, self.funimation_id, self.funimation_id, uid)
        return url