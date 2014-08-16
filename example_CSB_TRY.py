from SGS_bot import *
import sys
import time

class MyBot(SGS_bot):
    """
        books the first shift availible
        if a shift is already booked, try to book an earlier shift"
    """
    PANEL_ID = 19423
    BOOK_URL="https://portal.csbnet.se/mittomrade/tvattstuga/?"

    def login(self,pin):
        values = {'username' : self.USER,
                  'password' : pin
                 }
        url_values = urllib.urlencode(values)
        data = self.opener.open('https://portal.csbnet.se/en/',url_values)

    def try_to_book (self,date,interval,machines_id):
        """
            tries to book a shift
            returns True if shift was booked False otherwise
        """
#        if interval < 0 or interval > 7:
#            #invalid interval
#            return False
#        if self.booked_shift:
#            #impossible to book more then one shift
#            return False
        self.opener.addheaders = self.HEADERS.items() + [('Referer','https://portal.csbnet.se/mittomrade/tvattstuga/?')]
        values = {
                  'bookingptg' : '19423,123472,123483',
                  'panelid'    : str(self.PANEL_ID),
                  'show'       : 'true',
                  'intervalid' : str(interval),
                  'date'       : date,
                  'makeCancellation' : 'true',
                  'makeReservation'  : 'false'
                }
        url_values = urllib.urlencode(values)
        data = self.opener.open(self.BOOK_URL,url_values)
        data = self.opener.open(self.BOOK_URL,url_values)
        data = self.opener.open(self.BOOK_URL,url_values)
        print data.read()
        return True
        #different error pages may contains the following strings
        #ej bokningsbart
        #Max antal framtida pass
        #if "Bokningstider" in data.read():
        #    self.booked_shift = self.get_booked_shift()
        #    return True
        #else:
        #    return False

    def run(self):
        #shift = self.force_book_first_free_shift()
        #c = self.get_calendar(shift['week_offset'],shift['machines_id'])
        #print c
        self.try_to_book('2014-08-17',11,None)

    def object_number(self):
        return 503004325
    def user_number(self):
        #return 122182
        return 'user'
    def password(self):
        return 'pass'
if __name__ == '__main__':
    MyBot(hack_login=False)
