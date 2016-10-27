[![Code Climate](https://codeclimate.com/github/myles/telegram-myles-bot/badges/gpa.svg)](https://codeclimate.com/github/myles/telegram-myles-bot)

# [@MylesBot](https://telegram.me/MylesBot)

A Telegram Bot I created about me.

## Requirments

* [Telegram Bot](https://core.telegram.org/bots#3-how-do-i-create-a-bot)
* [Foursquare](https://developer.foursquare.com/)
* Python 2.7

## Development Environment Setup

You will need the following:

* Python 2.7
* pip
* virtualenvwrapper
* API Keys for Foursquare, Instagram, and Twitter

Start by cloning the repository:

```
$ git clone git@github.com:myles/telegram-myles-bot
$ cd ~/telegram-myles-bot
```

Create a Python virtual environment:

```
~/telegram-myles-bot $ mkvritualenv telegram-myles-bot
(telegram-myles-bot) ~/telegram-myles-bot $
```

The (telegram-myles-bot) prefix indicates that a virtual environment called
"telegram-myles-bot" is being used. Next, check that you have the correct
version of Python:

```
(telegram-myles-bot) ~/telegram-myles-bot $ python --version
Python 2.7.12
(telegram-myles-bot) ~/telegram-myles-bot $ pip --version
pip 8.0.2 from /Users/.../site-packages (python 2.7)
```

Install the project requirements:

```
(telegram-myles-bot) ~/telegram-myles-bot $ pip install -U -r requirements.txt
```

Create the configuration file at `config.json` that looks like:

```
{
  "telegram": "",
  "foursquare": {
    "client_id": "",
    "client_secret: "",
    "access_token": ""
  }
}
```
