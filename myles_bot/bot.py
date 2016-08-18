from telegram.parsemode import ParseMode
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from myles_bot import ext


class MylesBot(object):

    def __init__(self, config):
        self.config = config

        self.telegram_api_key = config['telegram']

        self.keyboard = [[KeyboardButton('Who is Myles?'),
                          KeyboardButton('Where is Myles?')]]

    def send_message(self, bot, update, msg, disable_link_preview=True):
        return bot.sendMessage(update.message.chat_id, msg,
                               reply_markup=ReplyKeyboardMarkup(self.keyboard),
                               resize_keyboard=True,
                               parse_mode=ParseMode.MARKDOWN,
                               disable_web_page_preview=disable_link_preview)

    def send_location(self, bot, update, latitude, longitude):
        reply_markup = ReplyKeyboardMarkup(self.keyboard)
        return bot.sendLocation(update.message.chat_id, latitude, longitude,
                                reply_markup=reply_markup,
                                resize_keyboard=True)

    def send_venue(self, bot, update, latitude, longitude, title, address,
                   **kwargs):
        return bot.sendVenue(update.message.chat_id, latitude, longitude,
                             title, address, resize_keyboard=True,
                             reply_markup=ReplyKeyboardMarkup(self.keyboard),
                             **kwargs)

    def command_who(self, bot, update):
        messages = [
            "Myles Braithwaite lives in Toronto where he runs a small "
            "consluting company called [Monkey in your Soul]"
            "(https://monkeyinyoursoul.com/) (you should hire him because "
            "he's awesome).",
            "You should follow him on [Twitter](https://twitter.com/mylesb) "
            "or [Instagram](https://instagram.com/myles).",
            "You can find his programming stuff on [GitHub]"
            "(https://github.com/myles) or [CodePen]"
            "(http://codepen.io/mylesb/)."
        ]

        for msg in messages:
            self.send_message(bot, update, msg)

    def command_where(self, bot, update):
        foursquare = ext.get_foursquare_location(self.config['foursquare'])
        venue = foursquare['venue']
        location = venue['location']

        msg = "Myles Braithwaite checked in to *{venue[name]}* {ago}."
        self.send_message(bot, update, msg.format(**foursquare))

        if location.get('address', None):
            self.send_venue(bot, update, location['lat'], location['lng'],
                            venue['name'], location['address'],
                            foursquare_id=venue['id'])
        else:
            self.send_location(bot, update, location['lat'], location['lng'])

    def command_tweet(self, bot, update):
        pass

    def command_photo(self, bot, update):
        pass

    def command_start(self, bot, update):
        msg = "Hi! I'm @MylesBot, a Telegram bot made by @MylesB about " \
              "@MylesB."

        self.send_message(bot, update, msg)

    def command_help(self, bot, update):
        messages = [
            "Available commands:",
            "`/who` - Who is Myles?",
            "`/where` - Where is Myles?",
            "`/tweet` - What was the last tweet Myles sent?",
            "`/photo` - What was the last Instagram photo Myles took?"
        ]

        for msg in messages:
            self.send_message(bot, update, msg)

    def noncommand_text(self, bot, update):
        text = update.message.text

        if text == 'Who is Myles?':
            self.command_who(bot, update)

        if text == 'Where is Myles?':
            self.command_where(bot, update)

    def run(self):
        updater = Updater(self.telegram_api_key)

        dp = updater.dispatcher

        dp.add_handler(CommandHandler('start', self.command_start))
        dp.add_handler(CommandHandler('help', self.command_help))

        dp.add_handler(CommandHandler('who', self.command_who))
        dp.add_handler(CommandHandler('where', self.command_where))

        dp.add_handler(CommandHandler('tweet', self.command_tweet))
        dp.add_handler(CommandHandler('photo', self.command_photo))

        dp.add_handler(MessageHandler([Filters.text], self.noncommand_text))

        updater.start_polling()
        updater.idle()
