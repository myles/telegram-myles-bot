from time import mktime
import datetime

import humanize
import feedparser


def get_last_feed_post(feed):
    feed = feedparser.parse(feed)
    entry = feed.entries[0] 

    published = datetime.datetime.fromtimestamp(mktime(entry.published_parsed))
    entry.ago = humanize.naturaltime(datetime.datetime.now() - published)

    return entry
