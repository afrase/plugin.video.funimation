# -*- coding: utf-8 -*-
import xbmc
from logging import Handler


class KodiHandler(Handler):

    def emit(self, record):
        try:
            msg = self.format(record)
            xbmc.log(msg.decode('utf8'))
        except:
            self.handleError(record)
