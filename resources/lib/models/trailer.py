from resources.lib.models.base_video import BaseVideo


class Trailer(BaseVideo):
    def __init__(self, json):
        super(Trailer, self).__init__(json)
