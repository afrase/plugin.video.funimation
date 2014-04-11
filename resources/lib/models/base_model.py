from resources.lib.utils import Utils


class BaseModel(object):
    def __init__(self, json):
        self.plugin = Utils().get_plugin()
        self.log = Utils().get_log
        self.json = json
        self.title = json['title']
        self.nid = json['nid']
        self.show_thumbnail = json['show thumbnail']