import sys
import os
import urllib
import datetime

USER='1234'
PASS='1234'

#Not sure what this means, maybe your aptus id? (seems to be static)
TYPE_ID=260685
#Probably this is the Id for Rotary (seems to be static)
GROUP_ID=267946
#uknown
PANEL_ID=48033

#Treshhold, maximum number of days
TRESH = 100

LOGIN_URL="https://www.sgsstudentbostader.se/Assets/Handlers/MOMENTUM.ashx"
BOOK_URL="https://tvatta.sgsstudentbostader.se/wwwashwait.aspx"

def main():
    opener = urllib.FancyURLopener({})
#    f = opener.open(LOGIN_URL)
#    if f.read() == "Logged in":
#        print "already loggid in"
#        print "trying to book shifts"
#    else:
#        doLogin()
    #doLogin()
    if book():
        print "booked a shift"
    else:
        print "booking failed"

def book():
    for i in range(0,TRESH):
        date = getDate(i)
        for interval in range(0,7):
            if try_to_book(date,interval):
                return True
    return False

def try_to_book (date,interval):
    if interval < 0 or interval > 7:
        #invalid interval
        return False
    opener = urllib.FancyURLopener({})
    f = opener.open(BOOK_URL + "?command=book&PanelId=" + str(PANEL_ID) + "&TypeId=" + str(TYPE_ID) + \
            "&GroupId=" + str(GROUP_ID) + "&Date=" + date + "&IntervalId=" + str(interval))
    print f.read()
    return True

#return a date string using format "yyyy-mm-dd"
#input is the day offset against the current date
def getDate(i):
    now = datetime.datetime.now() + datetime.timedelta(days=i)
    return ('%i-%02i-%02i' % (now.year,now.month,now.day))

#each day is diveded into 8 intervals (0-7), 4h*8 = 24h = 1 day
#return the current interval
def getInterval():
    return 0

def doLogin():
    isresident='true'
    customerid=USER
    loggedin='true'
    customerstatus='1'
    laundry='true'
    customerName='hej'
    laundry='trams'
    token=PASS
    gets = "isresident=" + isresident + \
           "&customerid=" + customerid + \
           "&loggedin=" + loggedin + \
           "&customerstatus=" + customerstatus + \
           "&tvattstuga=" + laundry + \
           "&customer_name=" + customerName + \
           "&token=" + token
    os.system("curl " + LOGIN_URL + '?' + gets)


if __name__ == '__main__':
    main()



#https://tvatta.sgsstudentbostader.se/wwwashwait.aspx?command=book&PanelId=48033&TypeId=260685&GroupId=267946&Date=2014-06-03&IntervalId=7

