from SGS_bot import *

if __name__ == '__main__':
    bot = SGS_bot(None)
    bot.hack_login()
    data = bot.get_calendar(0)
    print data.read()
