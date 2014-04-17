from resources.lib.controllers.base_controller import BaseController


class TrailersController(BaseController):
    def __init__(self, node, show_id=None, page='0'):
        super(TrailersController, self).__init__()