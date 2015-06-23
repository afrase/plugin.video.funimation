# -*- coding: utf-8 -*-
import os
import sys
import logging
import xbmc
import xbmcaddon
from resources.lib.kodi_handler import KodiHandler

addon = xbmcaddon.Addon()


def setup_logging():
    logger = logging.getLogger('funimation')
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '[{0}] %(funcName)s : %(message)s'.format(addon.getAddonInfo('id')))
    kh = KodiHandler()
    kh.setLevel(logging.DEBUG)
    kh.setFormatter(formatter)
    logger.addHandler(kh)
    return logger


def main():
    log = setup_logging()
    log.debug('ARGV: ' + repr(sys.argv))

    import resources.lib.nav as nav
    nav.list_menu()


if __name__ == '__main__':
    main()
