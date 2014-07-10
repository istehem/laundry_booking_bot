from SGS_bot import *

class MyBot(SGS_bot):
    def run(self):
        self.hack_login()
        data = self.get_calendar(0)
        print data.read()
    def object_number(self):
        return 503004325
    def user_number(self):
        return 122182

if __name__ == '__main__':
    MyBot()
