from resources.lib.models.base_model import BaseModel


class BaseVideo(BaseModel):
    def __init__(self, json):
        super(BaseVideo, self).__init__(json)
        get = self.json.get

        self.show_title = get('show title')
        self.funimation_id = get('Funimation ID')
        self.duration = self.utils.to_minutes(get('duration'))
        self.votes = get('votes', 0)
        self.rating = get('rating', 'NR')
        self.sub_dub = None

    def dub(self):
        return self.sub_dub == 'Dub'

    def sub(self):
        return self.sub_dub == 'Sub'