import re
import sys


class User(object):
    def __init__(self, json):
        self.common = sys.modules['__main__'].common
        self.json = json
        get = self.json.get

        if get('uid'):
            self.logged_in = True
            self.uid = get('uid')
            self.name = get('name')
            self.mail = get('mail')
            self.realname = get('realname')
            self.hostname = get('hostname')
            self.age = get('age')
            self.session = get('session')
            self.subscribed = get('roles').items()[0][1] == 'Subscriber'
            self.error_message = None
            self.common.log('logged in as "%s"' % self.name)
        else:
            self.logged_in = False
            self.name = get('roles')['1'].split(' ')[0]
            self.error_message = self.__extract_message__(json['session'])
            self.common.log('log in failed: %s' % self.error_message)

    def __extract_message__(self, msg):
        re_obj = re.compile('^.*?\"(.*?)\".*$')
        match = re_obj.search(msg)
        if match:
            self.common.log('found session results')
            return match.group(1)
        else:
            return None