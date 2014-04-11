import requests


class HttpClient(object):
    # __instance__ = None
    __req__ = None

    def __init__(self):
        if not self.__req__:
            self.__req__ = requests.Session()
            self.set_user_agent('FUNimation/858 CFNetwork/672.1.13 Darwin/14.0.0')
            self.__base_url = self.set_base_url('http://www.funimation.com')

    # def __new__(cls, *args, **kwargs):
    #     if not cls.__instance__:
    #         cls.__instance__ = super(HttpClient, cls).__new__(cls, *args)
    #     return cls.__instance__

    def set_user_agent(self, agent):
        self.__req__.headers['User-Agent'] = agent

    def set_base_url(self, url):
        self.__base_url = url
        return url

    def get(self, url, **kwargs):
        if url.startswith('/'):
            url = self.__url__(url)
        kwargs.setdefault('allow_redirects', True)
        return self.__req__.request('GET', url, **kwargs)

    def post(self, url, data=None, **kwargs):
        if url.startswith('/'):
            url = self.__url__(url)
        return self.__req__.request('POST', url, data=data, **kwargs)

    def get_cookie_dict(self):
        return self.__req__.cookies.get_dict()

    def update_cookie_jar(self, c_dict):
        self.__req__.cookies.update(c_dict)

    def __url__(self, path):
        return self.__base_url + path