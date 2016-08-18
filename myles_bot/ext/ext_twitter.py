import datetime

import tweepy
import humanize

def get_last_tweet(config):
    auth = tweepy.OAuthHandler(config['consumer_key'],
                               config['consumer_secret'])
    auth.set_access_token(config['access_token'],
                          config['access_token_secret'])

    t = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

    tweet = t.user_timeline(screen_name='mylesb', count=1,
                            exclude_replies=True, include_rts=False)[0]
    tweet['images'] = []

    created_at = datetime.datetime.strptime(tweet['created_at'],
                                            '%a %b %d %H:%M:%S +0000 %Y')
    tweet['ago'] = humanize.naturaltime(datetime.datetime.now() - created_at)

    for url in tweet['entities']['urls']:
        tweet['text'] = tweet['text'].replace(url['url'], url['expanded_url'])

    for media in tweet['entities']['media']:
        if media['type'] == 'photo':
            tweet['images'].append(media['media_url'])
            tweet['text'] = tweet['text'].replace(media['url'], '')

    return tweet
