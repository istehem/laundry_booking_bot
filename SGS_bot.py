import urllib
import urllib2
import datetime
import cookielib
import time
import abc

class SGS_bot:
    __metaclass__ = abc.ABCMeta

    USER='122182'
    PASS='1234'
    #The ocject number of your apartment
    OBJECT_NUMBER='503004325'

    #Not sure what this means, maybe your aptus id? (seems to be static)
    TYPE_ID=260685
    #Probably this is the Id for Rotary (seems to be static)
    GROUP_ID=267946
    #uknown
    PANEL_ID=48033

    BOOK_URL="https://tvatta.sgsstudentbostader.se/wwwashwait.aspx"
    CALENDAR_URL='https://tvatta.sgsstudentbostader.se/wwwashcalendar.aspx'
    LOGIN_URL="https://www.sgsstudentbostader.se/Assets/Handlers/Momentum.ashx"

    USE_HACK=True

    HEADERS = {
            'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64; rv:29.0) Gecko/20100101 Firefox/29.0 Iceweasel/29.0.1',
            'Accept' :  '*/*',
            'Accept-Encoding' : 'utf-8',
          }

    def __init__(self,use_hack=True):
        self.USE_HACK = use_hack
        self.opener = self.create_opener()
        self.run()

    def create_opener(self):
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        opener.addheaders = self.HEADERS.items()
        urllib2.install_opener(opener)
        return opener

    def getDate(self,i):
        now =    datetime.datetime.now() + datetime.timedelta(days=i)
        return ('%i-%02i-%02i' % (now.year,now.month,now.day))

    #each day is diveded into 8 intervals (0-7), 4h*8 = 24h = 1 day
    #first shift (0) starts at 01:00
    #return the current interval.
    def get_interval():
        now = datetime.datetime.now()
        return ((now.hour + 24 - 1) % 24) / 3

    def get_calendar(self,week_offset):
        values = {
            'panelId'    : str(self.PANEL_ID),
            'weekOffset' : str(week_offset),
            'type'       : str(self.TYPE_ID),
            'group'      : str(self.GROUP_ID)
             }
        url_values = urllib.urlencode(values)
        full_url = self.CALENDAR_URL + '?' + url_values
        data = self.opener.open(full_url)
        return data

    def login(self):
        raise NotImplementedError, "Implement login or use hack_login"

    #Security hole, allows this
    def hack_login(self):
        values = {'isresident': 'true',
              'loggedin'      : 'true',
              'customerid'    : self.USER,
              'tvattstuga'    : 'true',
              'customer_name' : self.OBJECT_NUMBER
             }
        url_values = urllib.urlencode(values)
        full_url = self.LOGIN_URL + '?' + url_values
        self.opener.open(full_url)
        self.opener.open('https://www.sgsstudentbostader.se/ext_gw.aspx?module=wwwash&lang=se?loggedin=true')
    @abc.abstractmethod
    def run(self):
        "starts the algorithm"
    @abc.abstractmethod
    def sleep(self):
        "should return an integer (seconds to sleep)"
