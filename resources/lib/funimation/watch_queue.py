import os
import json
import logging
from .models import Show, Video

__all__ = ['WatchQueue']
_log = logging.getLogger('funimation')


class WatchQueue(object):

    def __init__(self, dbpath):
        super(WatchQueue, self).__init__()
        self.dbpath = dbpath
        self._shows = []
        self._load()

    def add_show(self, show):
        if isinstance(show, Show):
            for s in self._shows:
                if s['asset_id'] == show.asset_id:
                    return
            self._shows.append(show.to_dict())
            _log.info('Added "{0}" to queue'.format(show.series_name))
        self._save()

    def remove_show(self, show_id):
        new_list = []
        for s in self._shows:
            if s['asset_id'] != show_id:
                new_list.append(s)
        self._shows = new_list
        self._save()

    @property
    def shows(self):
        return [Show(**s) for s in self._shows]

    def _load(self):
        if os.path.exists(self.dbpath):
            with open(self.dbpath, 'rb') as db:
                self._shows = json.load(db)

    def _save(self):
        with open(self.dbpath, 'wb') as db:
            json.dump(self._shows, db)
