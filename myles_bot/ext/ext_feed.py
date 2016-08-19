import datetime
from time import mktime

import humanize
import feedparser


def get_last_feed_post(feed):
    feed = feedparser.parse(feed)
    entry = feed.entries[0]

    published_epoch = mktime(entry.published_parsed)
    entry.published = datetime.datetime.fromtimestamp(published_epoch)
    entry.ago = humanize.naturaltime(datetime.datetime.now() -
                                     entry.published_parsed)

    return entry
