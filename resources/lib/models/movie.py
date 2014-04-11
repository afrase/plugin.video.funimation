from resources.lib.models import base_video


class Movie(base_video.BaseVideo):
    def __init__(self, json):
        super(Movie, self).__init__(json)
        self.rating = json['rating']