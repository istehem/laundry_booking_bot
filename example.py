from SGS_bot import *
import sys
import time

class MyBot(SGS_bot):
    """
        books the first shift availible
        if a shift is already booked, try to book an earlier shift"
    """
    def run(self):
        self.hack_login()
        week_offset = 0
        while True:
            booked_time = (-1,-1)
            d = self.get_calendar(0)
            terminate = False 
            while True:
                if terminate:
                    break
                for weekday in range(0,6):
                    if terminate:
                        break
                    for shift in range (0,8):
                        if (weekday, shift) in d['booked']:
                           booked_time = (weekday, shift)
                           print "already has the earliest shift booked\n"
                           terminate = True
                           break
                        if self.is_free_shift(week_offset, weekday,shift,d):
                            bs = self.get_booked_shift()
                            if bs != None:
                               self.try_to_unbook(bs['date'],bs['interval'])
                            if self.try_to_book(date, shift):
                                print "successfully booked shift " + str(shift) + " at " + date + "\n" 
                            else:
                                print "unable to book shift " + str(shift) + " at " + date + "\n" 
                            terminate = True
                            break
                week_offset = week_offset + 1
            d = self.get_calendar(week_offset-1)
            self.print_calendar(d)
            time.sleep(3600)
    def object_number(self):
        return 503004325
    def user_number(self):
        return 122182

if __name__ == '__main__':
    MyBot()
