from SGS_bot import *

class MyBot(SGS_bot):
    def sleep(self):
        return 100
    def run(self):
        pass

if __name__ == '__main__':
    MyBot()
