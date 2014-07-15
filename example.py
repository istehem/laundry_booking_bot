from SGS_bot import *
import sys
import time

class MyBot(SGS_bot):
    def run(self):
        self.hack_login()
        self.try_to_auto_unbook()
        if self.try_to_book(self.get_date(2),self.get_interval()):
            print "booked a shift"
            time.sleep(10)
            if self.try_to_auto_unbook():
                print "unbooked shift"
            else:
                #should never get here
                print "no shifts booked" 
        else:
            print "failed to book a shift"
    def object_number(self):
        return 503004325
    def user_number(self):
        return 122182

if __name__ == '__main__':
    MyBot()
