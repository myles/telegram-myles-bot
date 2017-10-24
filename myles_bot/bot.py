# coding=utf-8

import re
import string
from StringIO import StringIO

import requests

from telegram import KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
from telegram.parsemode import ParseMode

from . import ext

web_slug_regex = re.compile('^/web (?P<slug>[-\w,\.]+)$')
anlytics_code = "utm_source=telegram&utm_medium=bot&utm_campaign=MylesBot"


class MylesBot(object):

    def __init__(self, config):
        """
        :param config: a dictionary configuration of the bot.
        """

        self.config = config

        self.telegram_api_key = config['telegram']

        self.keyboard = [[KeyboardButton('Who is Myles?'),
                          KeyboardButton('Where is Myles?')],
                         [KeyboardButton("What was Myles' last tweet?"),
                          KeyboardButton("What was Myles' last photo?")]]

    def send_message(self, bot, update, msg, disable_link_preview=True,
                     **kwargs):
        """
        Send a message.

        :param msg: The message to send to the user.
        """

        return bot.sendMessage(update.message.chat_id, msg,
                               reply_markup=ReplyKeyboardMarkup(self.keyboard),
                               resize_keyboard=True,
                               parse_mode=ParseMode.MARKDOWN,
                               disable_web_page_preview=disable_link_preview,
                               **kwargs)

    def send_messages(self, bot, update, messages):
        """
        Send multiple messages to the user.

        :param messages: A list of messages to send to the user.
        """

        for msg in messages:
            self.send_message(bot, update, msg)

    def send_location(self, bot, update, lat, lon, **kwargs):
        """
        Send a location to the user.

        :param lat: The latitude to the location.
        :param lon: The longitude to the location.
        """

        reply_markup = ReplyKeyboardMarkup(self.keyboard)
        return bot.sendLocation(update.message.chat_id, lat, lon,
                                reply_markup=reply_markup,
                                resize_keyboard=True,
                                **kwargs)

    def send_venue(self, bot, update, lat, lon, title, address, **kwargs):
        """
        Send a venue location to the user.

        :param lat: The latitude to the venue's location.
        :param lon: The longitude to the venue's location.
        :param title: The title of the venue.
        :param address: The address of the venue's location.
        """

        return bot.sendVenue(update.message.chat_id, lat, lon, title, address,
                             reply_markup=ReplyKeyboardMarkup(self.keyboard),
                             resize_keyboard=True,
                             **kwargs)

    def send_photo(self, bot, update, photo, **kwargs):
        """
        Send a photo to the user.

        :param photo: The StringIO of the photo.
        """

        bot.sendChatAction(update.message.chat_id, action="upload_photo")
        return bot.sendPhoto(update.message.chat_id, photo=photo, **kwargs)

    def send_photo_url(self, bot, update, url):
        """
        A function for sending a photo by URL.

        :param url: The URL to the photograph.
        """

        resp = requests.get(url)
        return self.send_photo(bot, update, StringIO(resp.content))

    def command_who(self, bot, update):
        """When the command who runs."""

        messages = [
            'Myles Braithwaite lives in Toronto where he runs a small '
            'consluting company called [Monkey in your Soul]'
            '(https://monkeyinyoursoul.com/) (you should hire him because '
            "he's awesome).",
            'You should follow him on [Twitter](https://twitter.com/mylesb) '
            'or [Instagram](https://instagram.com/myles).',
            'You can find his programming stuff on [GitHub]'
            '(https://github.com/myles) or [CodePen]'
            '(http://codepen.io/mylesb/).'
        ]

        self.send_messages(bot, update, messages)

    def command_where(self, bot, update):
        """When the command where runs."""

        bot.sendChatAction(update.message.chat_id, action='typing')

        foursquare = ext.get_foursquare_location(self.config['foursquare'])
        venue = foursquare['venue']
        location = venue['location']

        msg = 'Myles Braithwaite checked in to *{venue[name]}* {ago}.'
        self.send_message(bot, update, msg.format(**foursquare))

        if location.get('address', None):
            self.send_venue(bot, update, location['lat'], location['lng'],
                            venue['name'], location['address'],
                            foursquare_id=venue['id'])
        else:
            self.send_location(bot, update, location['lat'], location['lng'])

    def command_tweet(self, bot, update):
        """When the command tweet runs."""

        bot.sendChatAction(update.message.chat_id, action='typing')

        tweet = ext.get_last_tweet(self.config['twitter'])

        for url in tweet.get('images', []):
            self.send_photo_url(bot, update, url)

        messages = [
            u'{text}',
            '[@{user[screen_name]}](https://twitter.com/{user[screen_name]}) '
            '- {ago}'
        ]

        for msg in messages:
            self.send_message(bot, update, msg.format(**tweet))

    def command_photo(self, bot, update):
        """When the command photo runs."""

        self.send_message(bot, update, "Not implemented yet.")

    def command_web(self, bot, update):
        """When the command web runs."""

        bot.sendChatAction(update.message.chat_id, action="typing")

        text = update.message.text
        webs = self.config['web']
        messages = []

        web_slug_match = web_slug_regex.match(text)

        if web_slug_match:
            slug = web_slug_match.group('slug')
            web = next((i for i in webs if i["slug"] == slug), None)

            post = ext.get_last_feed_post(web['feed_url'])

            if web.get('description'):
                messages.append("[{slug}]({url}) - *{name}* - "
                                "{description}".format(**web))
            else:
                messages.append("[{slug}]({url}) - *{name}*".format(**web))

            messages.append(u"[{title}]({link}) published "
                            "{ago}.".format(**post))
        else:
            messages.append("Where you can find Myles on the Web:")

            for web in webs:
                web['url'] = web['url'] + anlytics_code

                if web.get('description'):
                    messages.append("[{slug}]({url}) - *{name}* - "
                                    "{description}".format(**web))
                else:
                    messages.append("[{slug}]({url}) - *{name}*".format(**web))

        self.send_messages(bot, update, messages)

    def command_start(self, bot, update):
        """When the bot is started up and when the start command runs."""

        msg = ("Hi! I'm @MylesBot, a Telegram bot made by @MylesB about "
               "@MylesB.")

        self.send_message(bot, update, msg)

    def command_help(self, bot, update):
        """When the command help runs."""

        messages = [
            'Available commands:',
            '/who - Who is Myles?',
            '/where - Where is Myles?',
            '/tweet - What was the last tweet Myles sent?',
            '/photo - What was the last Instagram photo Myles took?',
            '/web - Where can I find Myles on the interwebs?',
        ]

        self.send_messages(bot, update, messages)

    def noncommand_text(self, bot, update):
        """What happens when the user does a non-command text."""

        # Get the message text and convert to lowercase
        text = update.message.text.lower()

        # Remove the punctutation
        punctuation = set(string.punctuation)
        text = ''.join(c for c in text if c not in punctuation)

        # 'Who' Command
        if text in ['who', 'who is myles', u'👱']:
            self.command_who(bot, update)

        # 'Where is Myles?' Command
        if text in ['where', 'where is myles', u'🕶', u'😎']:
            self.command_where(bot, update)

        # "What was Myles' Last Tweet" Command
        if text in ['tweet', 'twitter', 'what was myles last tweet', u'🐦']:
            self.command_tweet(bot, update)

        # "What was Myles' Last Photo" Command
        if text in ['photo', 'instagram', 'what was myles last photo', u'📷']:
            self.command_photo(bot, update)

        # 'Web' Command
        if text in ['web', 'website', 'websites', u'🌏', u'🌍', u'🌎']:
            self.command_web(bot, update)

        # 'Help' Command
        if text in ['help']:
            self.command_help(bot, update)

    def run(self):
        """Runs the Telegram Bot."""

        updater = Updater(self.telegram_api_key)

        dp = updater.dispatcher

        dp.add_handler(CommandHandler('start', self.command_start))
        dp.add_handler(CommandHandler('help', self.command_help))

        dp.add_handler(CommandHandler('who', self.command_who))
        dp.add_handler(CommandHandler('where', self.command_where))

        dp.add_handler(CommandHandler('tweet', self.command_tweet))
        dp.add_handler(CommandHandler('photo', self.command_photo))
        dp.add_handler(CommandHandler('web', self.command_web))

        dp.add_handler(MessageHandler([Filters.text], self.noncommand_text))

        updater.start_polling()
        updater.idle()
