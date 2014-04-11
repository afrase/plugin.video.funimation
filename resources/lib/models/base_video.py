from resources.lib.models import base_model


class BaseVideo(base_model.BaseModel):
    def __init__(self, json):
        super(BaseVideo, self).__init__(json)
        self.show_title = json['show title']
        self.funimation_id = json['Funimation ID']
        self.duration = json['duration'].split(':')[0]
        self.sub_dub = None

    def dub(self):
        return self.sub_dub == 'Dub'

    def sub(self):
        return self.sub_dub == 'Sub'