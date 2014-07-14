#!/usr/bin/python

import sys
import os
import urllib
import urllib2
import datetime
import cookielib
from SGS_bot import *


USER='122182'
PASS='1234'
#The ocject number of your apartment
OBJECT_NUMBER='503004325'

#Not sure what this means, maybe your aptus id? (seems to be static)
TYPE_ID=260685
#Probably this is the Id for Rotary (seems to be static)
GROUP_ID=267946
#uknown
PANEL_ID=48033

#Treshhold, maximum number of days
TRESH = 100

BOOK_URL="https://tvatta.sgsstudentbostader.se/wwwashwait.aspx"
CALENDAR_URL='https://tvatta.sgsstudentbostader.se/wwwashcalendar.aspx'
LOGIN_URL="https://marknad.sgsstudentbostader.se/API/Service/AuthorizationServiceHandler.ashx"
LOGIN_URL="https://www.sgsstudentbostader.se/Assets/Handlers/Momentum.ashx"
COOKIE_FILE="cookie.txt"

HEADERS = {
            'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64; rv:29.0) Gecko/20100101 Firefox/29.0 Iceweasel/29.0.1',
            'Accept' :  '*/*',
            'Accept-Encoding' : 'utf-8',
          }

def main():
    bot = SGS_bot(None)
    bot.hack_login()
    data = bot.get_calendar(0)
    print data.read()
    #opener = create_opener()
    #opener = hack_login(opener)
    #try_to_book(opener,getDate(3),get_interval())
    #data = get_calendar(opener,0)
    #data = get_calendar(opener,0)
    #print data.read()

def book(opener):
    for i in range(0,TRESH):
        date = getDate(i)
        for interval in range(0,7):
            if try_to_book(opener,date,interval):
                return True
    return False

def try_to_book (opener,date,interval):
    if interval < 0 or interval > 7:
        #invalid interval
        return False
    values = { 'command'    : 'book',
               'PanelId'    : str(PANEL_ID),
               'TypeId'     : str(TYPE_ID),
               'GroupId'    : str(GROUP_ID),
               'Date'       : date,
               'IntervalId' : str(interval),
               'NextPage'   : ''
            }
    url_values = urllib.urlencode(values)
    full_url = BOOK_URL + '?' + url_values
    data = opener.open(full_url)
    print full_url
    data = get_calendar(opener,0)
    print full_url
    return True

#return a date string using format "yyyy-mm-dd"
#input is the day offset against the current date
def getDate(i):
    now = datetime.datetime.now() + datetime.timedelta(days=i)
    return ('%i-%02i-%02i' % (now.year,now.month,now.day))

#each day is diveded into 8 intervals (0-7), 4h*8 = 24h = 1 day
#first shift (0) starts at 01:00
#return the current interval.
def get_interval():
   now = datetime.datetime.now()
   return ((now.hour + 24 - 1) % 24) / 3

def create_opener():
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    opener.addheaders = HEADERS.items()
    urllib2.install_opener(opener)
    return opener

#Security hole, allows this
def hack_login(opener):
    values = {'isresident'    : 'true',
              'loggedin'      : 'true',
              'customerid'    : USER,
              'tvattstuga'    : 'true',
              'customer_name' : OBJECT_NUMBER
             }
    url_values = urllib.urlencode(values)
    full_url = LOGIN_URL + '?' + url_values
    opener.open(full_url)
    data = opener.open('https://www.sgsstudentbostader.se/ext_gw.aspx?module=wwwash&lang=se?loggedin=true')
    return opener


def login(opener):
    return NotImplemented

def get_calendar(opener,week_offset):
    values = {
            'panelId'    : str(PANEL_ID),
            'weekOffset' : str(week_offset),
            'type'       : str(TYPE_ID),
            'group'      : str(GROUP_ID)
             }
    url_values = urllib.urlencode(values)
    full_url = CALENDAR_URL + '?' + url_values
    data = opener.open(full_url)
    return data

if __name__ == '__main__':
    main()
