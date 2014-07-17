from SGS_bot import *
import sys
import time

class MyBot(SGS_bot):
    """
        books the first shift availible
        if a shift is already booked, try to book an earlier shift"
    """
    def run(self):
#        while True:
            bs = self.force_book_first_free_shift()
            print ("booked shift is %i at %s") % (bs['interval'],bs['date'])
#            time.sleep(60)
    def object_number(self):
        return 503004325
    def user_number(self):
        return 122182

if __name__ == '__main__':
    MyBot(hack_login=True)
