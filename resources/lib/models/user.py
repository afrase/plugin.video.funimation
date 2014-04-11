from resources.lib.utils import Utils


class User(object):
    def __init__(self, json):
        self.json = json

        if any(x in json['session'] for x in ['incorrect', 'exist']):
            Utils().get_string('login_failed')
            self.__logged_in__ = False
            self.name = json['roles']['1'].split(' ')[0]
        else:
            self.__logged_in__ = True
            self.age = json['age']
            self.login = json['login']
            self.mail = json['mail']
            self.name = json['name']
            self.session = json['session']
            self.uid = json['uid']

    def logged_in(self):
        return self.__logged_in__