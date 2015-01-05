#Funimation XBMC Plugin

An XBMC plugin for streaming videos from funimation.com.

If you're interested in helping out, just drop me an email or send a pull
request. Patches and (constructive) input are always welcome.

Todo
----
+ implement a "My Watchlist"
+ better error handling
+ add more ways to browse shows
+ get show icons from different site
+ context menu for getting show details
+ switch to PS3 API because it appears to have higher resolution images and might be better developed.

Known issues
------------
Due to inconstancies in the API the plugin uses, sometimes you will get no
results back or an error from trying to get a list of videos. For example,
the JSON data returned by the API for getting the list of shows has a
`Video section` key which is supposed to indicate what kind of videos the show
has. This isn't always correct, the result for the show `Cowboy Bebop` has
`"Video section": {"1": "Episodes"}` but doesn't actually have any episodes.
