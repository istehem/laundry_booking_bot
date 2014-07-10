from SGS_bot import *

from Algorithm import Algorithm

class MyAlg(Algorithm):
    def sleep(self):
        return 100
    def run(self):
        pass

if __name__ == '__main__':
    alg = MyAlg()
    bot = SGS_bot(MyAlg())
    #bot.hack_login()
    #data = bot.get_calendar(0)
    #print data.read()
