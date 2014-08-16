from SGS_bot import *
import sys
import time

class MyBot(SGS_bot):
    """
        books the first shift availible
        if a shift is already booked, try to book an earlier shift"
    """
    def run(self):
        shift = self.force_book_first_free_shift()
        c = self.get_calendar(shift['week_offset'],shift['machines_id'])
        print c
    def object_number(self):
        return 503004325
    def user_number(self):
        return 122182

if __name__ == '__main__':
    MyBot(hack_login=True)
