class calendar:
    def __repr__(self):
        def color(text):
            colors = {
                     'BLUE'   : '\033[94m',
                     'GREEN'  : '\033[92m',
                     'YELLOW' : '\033[93m',
                     'RED'    : '\033[91m',
                     'ENDC'   : '\033[0m'
                     }
            return {
                   'free'     : colors['GREEN'] + text + colors['ENDC'],
                   'reserved' : colors['RED'] + text + colors['ENDC'],
                   'passed'   : colors['YELLOW'] + text + colors['ENDC'],
                   'booked'   : colors['BLUE'] + text + colors['ENDC']
                   }.get(text,text)
        days = {
                0 : 'Monday',
                1 : 'Tuesday',
                2 : 'Wednesday',
                3 : 'Thursday',
                4 : 'Friday',
                5 : 'Saturday',
                6 : 'Sunday'
               }
        try:
            l1  = "statuses for shifts %s using week offset %s" % (self.machines,self.week_offset) + '\n'
            l2  = '-'*81 + '\n'
            l3  = ("%-10s: " + "%-9i"*8) % tuple(["shift"] + range(0,8)) + '\n'
            l4  =  '-'*81 + '\n'
            lr  = ""
            for day in range(0,7):
                day_name = days[day]
                xs = [color(self.items[(day,shift)]['status']) for shift in range(0,8)]
                lr = lr  + ("%-10s: " + "%-17s "*8) % tuple([day_name] + xs) + '\n'
            return l1 + l2 + l3 + l4 + lr
        except:
            return "not a fully defined calendar object"

    statuses = {
            'free'     : [],
            'passed'   : [],
            'reserved' : [],
            'booked'   : []
               }
    machines_id = None
    machines    = None
    week_offset = None
    items       = dict()
