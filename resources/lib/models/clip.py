from resources.lib.models.base_video import BaseVideo


class Clip(BaseVideo):
    def __init__(self, json):
        super(Clip, self).__init__(json)
        self.rating = json['rating']