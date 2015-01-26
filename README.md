#Funimation XBMC Plugin

An XBMC plugin for streaming videos from funimation.com.

If you're interested in helping out, just drop me an email or send a pull
request. Patches and (constructive) input are always welcome.

PS3 API Information
-------------------
This just has some info about the API the PS3 app uses.

API endpoints
- Shows `/feeds/ps/shows`
- Episodes `/feeds/ps/videos`
- Featured Shows `/feeds/ps/featured`
- Login `/feeds/ps/login.json`
- Logout `/feeds/ps/logout`
- Main Screen Assests `/feeds/ps/getDeviceAssets`

---
#####Request info
`User-agent: Sony-PS3`

All requests have to have the query param ut=`user_type` from the login results, like ut=FunimationSubscriptionUser.

---
Here are the query params and values that I have found so far.
####shows
| Param        | Values                       |
| ------------ | ---------------------------- |
| ut           | FunimationSubscriptionUser   |
| limit        | int                          |
| offset       | int                          |
| sort         | SortOptionLatestSubscription |
| first-letter | a-z &#124; non-alpha         |
| filter       | FilterOptionSimulcast        |

####Episodes
| Param        | Values                       |
| ------------ | ---------------------------- |
| ut           | FunimationSubscriptionUser   |
| limit        | int                          |
| offset       | int                          |
| show_id      | int                          |

####Featured
| Param        | Values                       |
| ------------ | ---------------------------- |
| ut           | FunimationSubscriptionUser   |

---
####Login
post body 
playstation_id is always blank for some reason
```
{
    "username": "User",
    "password": "Password",
    "playstation_id": ""
}
```

returns
user_age appears to be off by one year...
```
{
    "user_id": "1234567",
    "user_type": "FUNIMATION_SUBSCRIPTION_USER",
    "user_birthday": "01-23-1991",
    "user_age": 22,
    "country": "US"
}
```

---
####Shows
```
[{
    "asset_id": "7556822",
    "pubDate": "08\/27\/2013",
    "series_name": "Cowboy Bebop",
    "link": "http:\/\/www.funimation.com\/cowboy-bebop",
    "series_description": "Explore the galaxy in this undeniably hip series that inspired a generation \u2013 and redefined anime as an indisputable art form. The Bebop crew is just trying to make a buck, and they\u2019re the most entertaining gang of bounty hunters in the year 2071.",
    "season_count": "1",
    "episode_count": 26,
    "genres": "Action,Sci Fi,Space",
    "simulcast": "0",
    "popularity": "4842",
    "official_marketing_website": "http:\/\/www.funimation.com\/cowboy-bebop",
    "latest_video_free": {
        "video_id": "57970",
        "release_date": "1417759200",
        "title": "Episode 4 (Dub)"
    },
    "latest_video_free_release_date": "1417759200",
    "latest_video_subscription": {
        "video_id": "58047",
        "release_date": "1417500000",
        "title": "Episode 26 (Dub)"
    },
    "latest_video_subscription_release_date": "1417500000",
    "show_rating": "TV-14",
    "active_hd_1080": "1",
    "thumbnail_small": "http:\/\/www.funimation.com\/admin\/uploads\/default\/shows\/show_thumbnail\/1_thumbnail\/CBY_thumb.jpg",
    "thumbnail_medium": "http:\/\/www.funimation.com\/admin\/uploads\/default\/shows\/show_mobile\/similar_shows\/CBY_mobile.jpg",
    "thumbnail_large": "http:\/\/www.funimation.com\/admin\/uploads\/default\/shows\/show_mobile\/1_device_show\/CBY_mobile.jpg",
    "poster_art": "http:\/\/www.funimation.com\/admin\/uploads\/default\/shows\/show_tv\/1_device_show\/CBY_tv_new.jpg",
    "contactLink": "http:\/\/www.funimation.com\/support",
    "display_order": 0,
    "element_position": 16,
    "languages": "Dub, Sub",
    "quality": "HD (1080)"
},]
```

---
####Episodes
```
{
  "videos" : [
    {
      "sequence" : "1",
      "quality" : "HD (1080)",
      "genre" : "Action,Sci Fi,Space",
      "tv_or_move" : "tv",
      "pubDate" : "11\/17\/2014",
      "url" : "asteroid-blues",
      "duration" : 1496,
      "description" : "Spike and Jet head to Tijuana to track down an outlaw smuggling a dangerous drug known as blood-eye.  Jet wants the bounty, but Spike has eyes for a far prettier prize.",
      "thumbnail_large" : "http:\/\/www.funimation.com\/admin\/uploads\/default\/recap_thumbnails\/7556822\/home_spotlight\/CBY0001.jpg",
      "closed_caption_location" : "",
      "show_name" : "Cowboy Bebop",
      "number" : 1,
      "releaseDate" : "2014\/11\/18",
      "featured" : "false",
      "highdef" : "true",
      "simulcast" : "0",
      "closed_captioning" : "0",
      "element_position" : 0,
      "display_order" : 0,
      "thumbnail" : "CBY0001.jpg",
      "has_subtitles" : "false",
      "extended_title" : "Cowboy Bebop : Episode 1 - Asteroid Blues (Dub)",
      "thumbnail_small" : "http:\/\/www.funimation.com\/admin\/uploads\/default\/recap_thumbnails\/7556822\/playlist\/CBY0001.jpg",
      "thumbnail_url" : "http:\/\/www.funimation.com\/admin\/uploads\/default\/recap_thumbnails\/7556822\/videos_spotlight\/CBY0001.jpg",
      "aips" : [
        "152.194",
        "758.091",
        "1009.425"
      ],
      "video_type" : "Episode",
      "dub_sub" : "dub",
      "popularity" : "4630",
      "video_url" : "http:\/\/wpc.8c48.edgecastcdn.net\/038C48\/SV\/480\/CBYENG0001\/CBYENG0001-480-,750,1500,2000,2500,4000,K.mp4.m3u8?9b303b6c62204a9dcb5ce5fdc007bb4104d2360e7fab15f96cf6e5f448e60394b08e9a09c51f786234bcd67b13e585ce7177b0a798e431722cf8aff5e61f5d2b274522d95cd9478b5d33afecce35f2cf1250c37930429ce355f94462",
      "asset_id" : "57967",
      "show_id" : "7556822",
      "title" : "Asteroid Blues",
      "language" : "en",
      "funimation_id" : "CBYENG0001",
      "rating" : "TV-14",
      "rating_system" : "tvpg",
      "thumbnail_medium" : "http:\/\/www.funimation.com\/admin\/uploads\/default\/recap_thumbnails\/7556822\/1_thumbnail\/CBY0001.jpg"
    }
  ]
}
```
