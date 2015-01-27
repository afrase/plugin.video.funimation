
class TemplateModel(object):
    _common_fields = [
        'asset_id',
        'display_order',
        'element_position',
        'popularity',
        'pubDate',
        'quality',
        'simulcast',
        'thumbnail_large',
        'thumbnail_medium',
        'thumbnail_small',
    ]

    _fields = []

    def __init__(self, **kwargs):
        self._fields.extend(self._common_fields)
        for k, v in kwargs.iteritems():
            if k in self._fields:
                try:
                    setattr(self, k, v)
                except Exception, e:
                    print(k, v)
                    raise e

    @property
    def icon(self):
        return self.thumbnail_large

    @property
    def label(self):
        return NotImplementedError()

    @property
    def query_string(self):
        raise NotImplementedError()

    @property
    def stream_info(self):
        if self.video_quality == 4000:
            w, h = 1920, 1080
        elif self.video_quality == 3500:
            w, h = 1080, 720
        else:
            w, h = 640, 480
        aspect = w / float(h)

        si = {
            'codec': 'mp4',
            'aspect': aspect,
            'width': w,
            'height': h,
            'duration': self.duration
        }

        return si

    def get(self, key, default=None):
        return getattr(self, key, default)

    # not sure if i like this, might show to much info
    def __repr__(self):
        return repr(self.__dict__)


class Show(TemplateModel):
    _fields = [
        'series_name',
        'link',
        'series_description',
        'season_count',
        'episode_count',
        'genres',
        'official_marketing_website',
        'latest_video_free',
        'latest_video_free_release_date',
        'latest_video_subscription',
        'latest_video_subscription_release_date',
        'show_rating',
        'active_hd_1080',
        'poster_art',
        'contactLink',
        'languages',
    ]

    @property
    def thumbnail(self):
        return self.poster_art

    @property
    def label(self):
        return self.series_name

    @property
    def label2(self):
        return '[]'

    @property
    def vtypes(self):
        return 'episodes'

    @property
    def info(self):
        video_info = {
            'genre': self.genres,
            'votes': self.popularity,
            'plot': self.series_description,
            'episode': self.episode_count,
            'aired': self.pubDate.strftime('%Y-%m-%d'),
            'year': self.pubDate.strftime('%Y'),
        }

        return video_info

    @property
    def query_string(self):
        qry = {
            'show_id': self.asset_id,
            'folder': 'true',
            'path': '/show/episodes',
            'get': 'episodes',
            'vtypes': self.vtypes,
        }

        return qry

    @property
    def stream_info(self):
        raise NotImplementedError()

    @property
    def sub(self):
        raise NotImplementedError()

    @property
    def dub(self):
        raise NotImplementedError()


class Episode(TemplateModel):
    _fields = [
        'aips',
        'closed_caption_location',
        'closed_captioning',
        'description',
        'dub_sub',
        'duration',
        'extended_title',
        'featured',
        'funimation_id',
        'genre',
        'has_subtitles',
        'highdef',
        'language',
        'number',
        'rating',
        'rating_system',
        'releaseDate',
        'sequence',
        'show_id',
        'show_name',
        'simulcast',
        'thumbnail_url',
        'title',
        'tv_or_move',
        'url',
        'video_type',
        'video_url',
    ]

    @property
    def label(self):
        if self.number:
            lbl = '%d. %s (%s)' % (self.number, self.title, self.dub_sub)
        else:
            lbl = '%s (%s)' % (self.title, self.dub_sub)
        return lbl

    @property
    def thumbnail(self):
        return self.thumbnail_url

    @property
    def sub(self):
        return self.dub_sub == 'sub'

    @property
    def dub(self):
        return self.dub_sub == 'dub'

    @property
    def info(self):
        video_info = {
            'duration': self.duration / 60,
            'episode': self.episode_number,
            'votes': self.votes,
            'genre': self.genre,
            'plot': self.description,
            'aired': self.pubDate.strftime('%Y-%m-%d'),
            'tvshowtitle': self.show_title,
        }

        return video_info

    @property
    def video_quality(self):
        if self.quality == 'HD (1080)':
            return 4000
        elif self.quality == 'HD (720)':
            return 3500
        else:
            return 2000

    @property
    def query_string(self):
        qry = {
            'id': self.asset_id,
            'path': '/show/episodes',
            'videoid': self.funimation_id,
        }

        return qry
