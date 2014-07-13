from SGS_bot import *
import sys

class MyBot(SGS_bot):
    def run(self):
        self.hack_login()
        if self.try_to_book(self.get_date(1),self.get_interval()):
            print "success"
        else:
            print "fail"
    def object_number(self):
        return 503004325
    def user_number(self):
        return 122182

if __name__ == '__main__':
    MyBot()
