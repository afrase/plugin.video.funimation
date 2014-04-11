from resources.lib.models import base_video


class Trailer(base_video.BaseVideo):
    def __init__(self, json):
        super(Trailer, self).__init__(json)
