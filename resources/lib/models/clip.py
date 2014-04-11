from resources.lib.models import base_video


class Clip(base_video.BaseVideo):
    def __init__(self, json):
        super(Clip, self).__init__(json)
        self.rating = json['rating']