import datetime

import humanize
from foursquare import Foursquare


def get_foursquare_location(config):
    f = Foursquare(client_id=config['client_id'],
                   client_secret=config['client_secret'],
                   access_token=config['access_token'])

    checkins = f.users.checkins(params={'limit': 1, 'sort': 'newestfirst'})
    checkin = checkins['checkins']['items'][0]

    created_at = datetime.datetime.fromtimestamp(int(checkin['createdAt']))

    checkin['ago'] = humanize.naturaltime(datetime.datetime.now() - created_at)

    return checkin
