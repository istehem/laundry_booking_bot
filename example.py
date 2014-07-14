from SGS_bot import *
import sys

class MyBot(SGS_bot):
    def run(self):
        #self.hack_login()
#        if self.try_to_book(self.get_date(0),5):
#            print "booked a shift"
#        else:
#            print "failed to book a shift"
#        if self.try_to_unbook(self.get_date(0),5):
#            print "unbooked a shift"
#        else:
#            print "failed to unbook a shift"
        self.get_booked_shift()
    def object_number(self):
        return 503004325
    def user_number(self):
        return 122182

if __name__ == '__main__':
    MyBot()
