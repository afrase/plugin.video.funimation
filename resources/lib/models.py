
class TemplateModel(object):
    _common_fields = ['total', 'title', 'nid', 'show_thumbnail', 'votes']
    _fields = []

    def __init__(self, **kwargs):
        self._fields.extend(self._common_fields)
        for k, v in kwargs.iteritems():
            if k in self._fields:
                setattr(self, k, v)

    @property
    def icon(self):
        return self.show_thumbnail

    @property
    def thumbnail(self):
        return self.show_thumbnail

    @property
    def label(self):
        return self.title

    @property
    def query_string(self):
        raise NotImplementedError()

    def get(self, key, default=None):
        return getattr(self, key, default)


class Show(TemplateModel):
    _fields = ['all_terms', 'maturity_rating', 'mobile_banner_large',
               'post_date', 'show_thumbnail_accedo', 'similar_shows',
               'video_section']

    @property
    def thumbnail(self):
        return self.mobile_banner_large

    @property
    def label2(self):
        return '[' + self.maturity_rating + ']'

    @property
    def vtypes(self):
        return ','.join([i.lower() for i in self.video_section])

    @property
    def info(self):
        video_info = {'genre': ', '.join(self.all_terms), 'votes': self.votes,
                      'aired': self.post_date.strftime('%Y-%m-%d'),
                      'year': self.post_date.strftime('%Y')}
        return video_info

    @property
    def query_string(self):
        qry = {'folder': 'true', 'id': self.nid, 'path': '/show',
        'vtypes': self.vtypes}
        return qry


class Episode(TemplateModel):
    _fields = ['aip', 'duration', 'episode_number', 'episode_thumbnail',
               'exclusive', 'funimation_id', 'language', 'promo', 'rating',
               'show_title', 'sub_dub', 'type', 'video_quality',
               'video_thumbnail_accedo']

    @property
    def label(self):
        return '%d. %s (%s)' % (self.episode_number, self.title, self.sub_dub)

    @property
    def thumbnail(self):
        return self.episode_thumbnail

    @property
    def hd(self):
        if 'HD (720)' in self.video_quality:
            return True
        else:
            return False

    @property
    def info(self):
        video_info = {'duration': self.duration,
                      'episode': self.episode_number, 'votes': self.votes,
                      'tvshowtitle': self.show_title}
        return video_info

    @property
    def query_string(self):
        qry = {'id': self.nid, 'path': '/show/episodes', 'videoid': self.funimation_id}
        return qry


class Movie(TemplateModel):
    _fields = ['aip', 'duration', 'funimation_id', 'language',
               'mobile_banner_large', 'promo', 'rating', 'show_title',
               'sub_dub', 'term', 'tv_key_art', 'video_quality',
               'video_thumbnail_accedo']

    @property
    def hd(self):
        if 'HD (720)' in self.video_quality:
            return True
        else:
            return False

    @property
    def info(self):
        video_info = {'duration': self.duration, 'votes': self.votes,
                      'mpaa': self.rating}
        return video_info

    @property
    def query_string(self):
        qry = {'id': self.nid, 'path': '/show/episodes', 'videoid': self.funimation_id}
        return qry


class Clip(TemplateModel):
    _fields = ['duration', 'funimation_id', 'funimationid', 'post_date',
               'rating', 'show_id', 'show_title', 'term', 'type',
               'video_thumbnail_accedo']

    @property
    def hd(self):
        return False

    @property
    def query_string(self):
        qry = {'id': self.nid, 'path': '/show/episodes', 'videoid': self.funimation_id}
        return qry


class Trailer(TemplateModel):
    _fields = ['duration', 'funimation_id', 'is_mature', 'show_title',
               'video_quality', 'video_thumbnail_accedo']

    @property
    def hd(self):
        if 'HD (720)' in self.video_quality:
            return True
        else:
            return False

    @property
    def query_string(self):
        qry = {'id': self.nid, 'path': '/show/episodes', 'videoid': self.funimation_id}
        return qry


class ShowDetail(TemplateModel):
    _fields = ['aspect_ratio', 'body', 'featured_product', 'genre',
               'has_episodes', 'has_subscription', 'has_videos', 'is_featured',
               'maturity_rating', 'mobile_banner_large', 'official_trailer',
               'path', 'post_date', 'similar_shows', 'teaser', 'tv_key_art',
               'type', 'updated_date', 'video_types']


class EpisodeDetail(TemplateModel):
    _fields = ['aip', 'aspect_ratio', 'body', 'duration', 'episode_number',
               'funimation_id', 'genre', 'group_nid', 'group_path',
               'group_title', 'maturity_rating', 'path', 'post_date',
               'quality', 'sequence_number', 'sub_dub',
               'subscription_sunrise_date', 'subscription_sunset_date',
               'sunrise_date', 'sunset_date', 'teaser', 'type', 'updated_date',
               'video', 'video_quality']
