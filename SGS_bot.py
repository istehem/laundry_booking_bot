import urllib
import urllib2
import datetime
import cookielib
import time
import abc
import sys
import re

class SGS_bot:
    __metaclass__ = abc.ABCMeta

    #: Not sure what this means, maybe your aptus id? (seems to be static) """
    TYPE_ID=260685
    #Probably this is the Id for Rotary (seems to be static)
    GROUP_ID=267946
    #uknown
    PANEL_ID=48033

    BOOK_URL="https://tvatta.sgsstudentbostader.se/wwwashcommand.aspx"
    CALENDAR_URL='https://tvatta.sgsstudentbostader.se/wwwashcalendar.aspx'
    LOGIN_URL="https://www.sgsstudentbostader.se/Assets/Handlers/Momentum.ashx"
    BOOKINGS_URL="https://tvatta.sgsstudentbostader.se/wwwashbookings.aspx"

    HEADERS = {
            'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64; rv:29.0) Gecko/20100101 Firefox/29.0 Iceweasel/29.0.1',
            'Accept' :  '*/*',
            'Accept-Encoding' : 'utf-8',
          }

    def __init__(self):
        self.opener = self.create_opener()
        self.USER = str(self.user_number())
        self.OBJECT_NUMBER=str(self.object_number())
        self.run()

    def create_opener(self):
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        opener.addheaders = self.HEADERS.items()
        urllib2.install_opener(opener)
        return opener

    def try_to_book (self,date,interval):
        """
            tries to book a shift
            returns True if shift was booked False otherwise
        """
        if interval < 0 or interval > 7:
            #invalid interval
            return False
        values = {'command'    : 'book',
                  'PanelId'    : str(self.PANEL_ID),
                  'TypeId'     : str(self.TYPE_ID),
                  'GroupId'    : str(self.GROUP_ID),
                  'Date'       : date,
                  'IntervalId' : str(interval),
                  'NextPage'   : ''
                 }
        url_values = urllib.urlencode(values)
        full_url = self.BOOK_URL + '?' + url_values
        data = self.opener.open(full_url)

        #different error pages may contains the following strings
        #ej bokningsbart
        #Max antal framtida pass

        return "Bokningstider" in data.read()

    def try_to_auto_unbook(self):
        """
            unbooks booked shift
            slower then try_to_book, since it must check for booked shift
            returns None if the shift as already started (SGS crap)
        """
        d = self.get_booked_shift()
        if not d:
           return False
        else:
           return self.try_to_unbook(d['date'],d['interval'])

    def try_to_unbook(self,date,interval):
        """
            tries to unbook a shift
            returns True if shift was unbooked False otherwise
        """
        if interval < 0 or interval > 7:
            #invalid interval
            return False
        values = {'command'    : 'cancel',
                  'PanelId'    : str(self.PANEL_ID),
                  'TypeId'     : str(self.TYPE_ID),
                  'GroupId'    : str(self.GROUP_ID),
                  'Date'       : date,
                  'IntervalId' : str(interval),
                  'NextPage'   : ''
                 }
        url_values = urllib.urlencode(values)
        full_url = self.BOOK_URL + '?' + url_values
        data = self.opener.open(full_url)

        #different error pages may contains the following strings
        #There is no row at position 0.

        return "Bokningstider" in data.read()

    def get_booked_shift(self):
        """
            if a shift is booked return a dict containing the date,
            booked machines and interval otherwise return None
        """
        data = self.opener.open(self.BOOKINGS_URL)
        html = html = data.read()
        cleanr = re.compile('<.*?>')
        text = re.sub(cleanr,'',html)
        m = re.search('rden(\d\d\d\d-\d\d-\d\d).*(\d-\d)(\d\d):\d\d-\d\d:\d\d',text)
        d = dict()
        if m:
            d['date']     = m.group(1)
            d['machines'] = m.group(2)
            #group 3 is the hour when the shift starts
            d['interval'] = ((int(m.group(3)) + 24 - 1) % 24) / 3
        else:
            d = None
        return d

    def get_date(self,i):
        """ returns the current date with offset i """
        now = datetime.datetime.now() + datetime.timedelta(days=i)
        return ('%i-%02i-%02i' % (now.year,now.month,now.day))

    def get_date_from_wd(self, week_offset, day):
        """
            returns the current date from week offset and week day
            if week_day > 6 return Null
            both input parameters should be of type int
        """
        if day > 6 or day < 0:
            #invalid date
            return None
        current_day = datetime.datetime.today().weekday()
        then = datetime.datetime.now() + datetime.timedelta(days=7*week_offset + day - current_day)
        return ('%i-%02i-%02i' % (then.year,then.month,then.day))

    def get_interval(self):
        """
        each day is diveded into 8 intervals (0-7), 4h*8 = 24h = 1 day
        first shift (0) starts at 01:00
        returns the current interval.
        """
        now = datetime.datetime.now()
        return ((now.hour + 24 - 1) % 24) / 3

    def get_calendar(self,week_offset):
        """ should return free shifts for a week """
        values = {
            'panelId'    : str(self.PANEL_ID),
            'weekOffset' : str(week_offset),
            'type'       : str(self.TYPE_ID),
            'group'      : str(self.GROUP_ID)
             }
        url_values = urllib.urlencode(values)
        full_url = self.CALENDAR_URL + '?' + url_values
        data = self.opener.open(full_url)
        html = data.read()
        r = re.compile('<img src="images/icon.*?gif.*?>')
        xs = r.findall(html)
        d = {
               'free'     : [],
               'passed'   : [],
               'reserved' : [],
               'booked'   : []
            }

        r = re.compile('icon_(.*?)\.gif')
        statuses = {
                    'plus'   : 'free',
                    'no'     : 'reserved',
                    'no_not' : 'passed',
                    'own'    : 'booked'
                   }
        for i, row in enumerate(xs):
            text = r.search(row).group(1)
            text = statuses[text]
            d[(i % 7, i / 7)] = text
            ys = d[text]
            ys.append((i % 7, i / 7))
            d[text] = ys

        return d

    def get_free_shifts(self,week_offset,calendar_dict=None):
        if calendar_dict == None:
            free =  self.get_calendar(week_offset)['free']
        else:
            free = calendar_dict['free']
        return free

    def get_first_free_shift(week_offset,d=None):
        xs = get_free_shifts(self,week_offset,d):
        if xs:
            return sorted(xs)[0]
        else:
            return None

    def print_calendar(self,calendar_dict):
        days = {
                0 : 'Monday',
                1 : 'Tuesday',
                2 : 'Wednesday',
                3 : 'Thursday',
                4 : 'Friday',
                5 : 'Saturday',
                6 : 'Sunday'
               }
        print ("%-10s: " + "%-11i"*8) % tuple(["shift "] + range(0,8))
        print '-'*95
        for day in range(0,7):
            day_name = days[day]
            xs = [calendar_dict[(day,shift)] for shift in range(0,8)]
            print ("%-10s: " + "%-10s "*8) % tuple([day_name] + xs)

    def is_free_shift(self,week_offset,day,shift,calendar_dict=None):
        if calendar_dict == None:
            b = (day,shift) in self.get_free_shifts(week_offset)
        else:
            b = (day,shift) in self.get_free_shifts(week_offset,calendar_dict)
        return b

    def login(self,pin):
        """ not implemented yet, raises and error """
        raise NotImplementedError, "Implement login or use hack_login"

    def hack_login(self):
        """ logs in to the booking system
            this is hack and works due to a security hole
        """
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
        """ abstract method
            starts the algorithm
        """
    @abc.abstractmethod
    def object_number(self):
        """ abstract method
            should return an integer specifying an object number for the apartment
        """
    @abc.abstractmethod
    def user_number(self):
        """ abstract method
            should return an integer specifying an user number
        """


