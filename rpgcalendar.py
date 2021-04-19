'''Simple RPG calendar, with 7 day week, 4 weeks per month,
3 months per season, 4 seasons per year.

The calendar starts at year zero by default. The lunar phase calculation
reflects that. Year 0, 4, 8, ... are waxing moons.
There are 7*4*3*4 = 336 days per year in this Calendar, ~92% of a year.

Seasons line up with the numbers of the months and as such it's more readable.

The lunar phases are by default weekly, though for my own game I created the
option of having a lunar phase that operated yearly instead.

The choice of "back" for "backwards" is for brevity.'''

_lunar_phases = {1:'waxing', 2:'full', 3:'waning', 4:'new'}
_seasons = {1:'spring', 2:'summer', 3:'fall', 4:'winter'}
_months = {1:'springswax', 2:'springtide', 3:'springswane',
           4:'summerswax', 5:'summertide', 6:'summerswane',
           7:'fallswax', 8:'falltide', 9:'fallswane',
           10:'winterswax', 11:'wintertide', 12:'winterswane'}
_days_per_week = 7
_weeks_per_month = 4
_months_per_year = len(_months)
_seasons_per_year = len(_seasons)
_lunar_phases_per_cycle = len(_lunar_phases)


def ordinal(num=0):
    'Returns ordinal number, e.g. 21st, from integer.'
    ord_end = num % 10
    if ord_end == 1:
        return str(num) + 'st'
    elif ord_end == 2:
        return str(num) + 'nd'
    elif ord_end == 3:
        return str(num) + 'rd'
    else:
        return str(num) + 'th'


class Calendar:
    def __init__(self, day=1, week=1, month=1, year=0):
        self.day = day
        self.week = week
        self.month = month
        self.year = year
        self.update_season()
        self.update_lunar_phase()

    def forward_year(self):
        self.year += 1
        # Do not remove: called here to apply to the YearlylunarPhase class.
        self.update_lunar_phase()

    def forward_years(self, years=1):
        self.year += years
        self.update_lunar_phase()
        
    def back_year(self):
        self.year -= 1

    def back_years(self, years=1):
        self.year -= years

    def forward_lunar_phase(self):
        '''Weekly lunar phases, puts you at start of next week.'''
        self.day = 1
        self.forward_week()

    def back_lunar_phase(self):
        '''Weekly lunar phases, puts you at start of previous week.'''
        self.day = 1
        self.back_week()

    def update_lunar_phase(self):
        # Because both week and lunar phase start at 1, modular
        # division results in zero modulus in the 4th lunar phase.
        self.lunar_phase = self.week % _lunar_phases_per_cycle
        if self.lunar_phase == 0:
            self.lunar_phase = 4

    def day_of_month(self):
        '''Returns the day of the month, as per normal calendar.'''
        # Weeks starts at 1 
        return (self.week - 1) * _days_per_week + self.day

    def back_week(self):
        self.week -= 1
        if self.week < 1:
            self.week = _weeks_per_month
            self.back_month()
        self.update_lunar_phase()
    
    def back_weeks(self, weeks=1):
        for w in range(weeks):
            self.back_week()

    def forward_week(self):
        self.week += 1
        if self.week > _weeks_per_month:
            self.week = 1
            self.forward_month()
        self.update_lunar_phase()
    
    def forward_weeks(self, weeks=1):
        for w in range(weeks):
            self.forward_week()

    def back_day(self):
        self.day -= 1
        if self.day < 1:
            self.day = _days_per_week
            self.back_week()

    def back_days(self, days=1):
        for d in range(days):
            self.back_day()
                
    def back_month(self):
        self.month -= 1
        if self.month < 1:
            self.month = _months_per_year
            self.back_year()
        self.update_season()
    
    def back_months(self, months=1):
        for m in range(months):
            self.back_month()

    def forward_season(self):
        '''This is akin to moving forward to the start of next season,
rather than moving forward three months.'''
        self.day = 1
        self.week = 1
        self.lunar_phase = 1
        if self.season == 1:
            self.month = 4
        elif self.season == 2:
            self.month = 7
        elif self.season == 3:
            self.month = 10
        else:
            self.month = 1
            self.forward_year()
        self.update_season()

    def back_season(self):
        '''Go to the start of the previous season.'''
        self.day = 1
        self.week = 1
        self.lunar_phase = 1
        if self.season == 1:
            self.month = 10
            self.back_year()            
        elif self.season == 2:
            self.month = 1
        elif self.season == 3:
            self.month = 4
        else:
            self.month = 7
        self.update_season()
    
    def forward_day(self):
        self.day += 1
        if self.day > _days_per_week:
            self.day = 1
            self.forward_week()

    def forward_days(self, days=1):
        for d in range(days):
            self.forward_day()
                
    def forward_month(self):
        self.month += 1
        if self.month > _months_per_year:
            self.month = 1
            self.forward_year()
        self.update_season()
    
    def forward_months(self, months=1):
        for m in range(months):
            self.forward_month()

    def update_season(self):
        if self.month in [1,2,3]:
            self.season = 1
        elif self.month in [4,5,6]:
            self.season = 2
        elif self.month in [7,8,9]:
            self.season = 3
        else:
            self.season = 4

    def report_long_and_tall(self):
        rep = f'Day: {self.day}\nWeek: {self.week}\nMonth: {self.month}\n'
        rep += f'Year: {self.year}\nSeason: {self.season}\n'
        rep += f'Lunar Phase: {self.lunar_phase}\n\n'
        return rep


    def report_one_liner(self):
        # Capitalizes the lunar phase.
        rep = f'Day {self.day}, Week {self.week}, Month {self.month}, ' + \
              f'Year {self.year}. ' + \
              f'Lunar Phase: {_lunar_phases[self.lunar_phase].title()}.'
        return rep

    def report_immersive(self):
        '''Provides descriptive one-liner report of date.'''
        dayout = ordinal(self.day_of_month())
        monthout = _months[self.month].title()
        seasonout = _seasons[self.season].title()
        moonout = _lunar_phases[self.lunar_phase]
        rep = f'It is the {dayout} of {monthout}, of the year ' + \
              f'{self.year}. It is {seasonout} and the moon is {moonout}.'
        return rep

    def month_of_season(self):
        months_per_season = _months_per_year // _seasons_per_year
        assert _months_per_year % _seasons_per_year == 0, \
               'Strange number of months in a year, vs. seasons.'
        return self.month % months_per_season
    
    def report_farmers(self):
        '''Provides descriptive one-liner report of date.'''
        dayout = ordinal(self.day)
        weekout = ordinal(self.week)
        monthout = ordinal(self.month_of_season())
        seasonout = _seasons[self.season].title()
        moonout = _lunar_phases[self.lunar_phase]
        rep = f'It is the {dayout} day of the {weekout} week of the ' + \
              f'{monthout} month of {seasonout}. The moon is {moonout}.'
        return rep

    def report_machine(self):
        '''Hopefully this is most convenient for use with other programs.'''
        return f'{self.day},{self.week},{self.month},{self.year},' + \
               f'{self.season},{self.lunar_phase}'

    def report_machine_DOM(self):
        '''Hopefully this is also convenient for use with other programs.
It uses day of month.'''
        return f'{self.day_of_month()},{self.week},{self.month},{self.year},' + \
               f'{self.season},{self.lunar_phase}'

    def generation_args(self):
        '''Use the returned list to generate another calendar, if you want.'''
        return [self.day, self.week, self.month, self.year]

class YearlyLunarPhase(Calendar):
    '''In this calendar, a lunar phase lasts an entire year, so there's a
year of waxing moon, a year of full moon, a year of waning moon, then
finally a year of new moon.'''
    # There are some unnecessary methods called in the general class,
    # e.g. update_lunar_phase() to fit this class, but I think that's fine.

    def forward_lunar_phase(self):
        '''This is akin to moving forward to the start of next year,
rather than moving forward one years.'''
        self.day = 1
        self.week = 1
        self.month = 1
        self.season = 1
        self.forward_year()    

    def back_lunar_phase(self):
        '''Go to the start of the previous lunar_phase, essentially
the last year.'''
        self.day = 1
        self.week = 1
        self.month = 1
        self.season = 1
        self.back_year()

    def update_lunar_phase(self):
        '''This assumes that the year starts at year zero, currently.'''
        # This works because the year starts at zero and lunar
        # phase starts at 1.
        self.lunar_phase = self.year % _lunar_phases_per_cycle + 1


def test_normal_calendar():
    c = Calendar()
    print(c.report_immersive())
    c.forward_days(6)
    print(c.report_farmers())
    c.forward_day()
    print(c.report_immersive())
    c.forward_week()
    print(c.report_immersive())
    c.forward_week()
    print(c.report_immersive())
    c.forward_year()
    print(c.report_immersive())
    c.forward_lunar_phase()
    print(c.report_immersive())
    c.forward_lunar_phase()
    print(c.report_immersive())
    c.forward_season()
    print(c.report_immersive())
    c.back_weeks(2)
    print(c.report_immersive())

def test_odd_calendar():
    c = YearlyLunarPhase()
    print(c.report_long_and_tall())
    c.forward_days(8)
    print(c.report_long_and_tall())
    c.forward_weeks(2)
    print(c.report_long_and_tall())
    print(c.day_of_month())
    c.forward_months(4)
    print(c.report_long_and_tall())
    c.forward_months(8)
    print(c.report_long_and_tall())
    print(c.report_one_liner())
    print(c.report_immersive())
    print(c.report_farmers())
    print(c.report_machine())
    print(c.report_machine_DOM())
    print(c.generation_args())
    c.forward_years(2)
    print(c.generation_args())
    print(c.report_farmers())
    
if __name__ == '__main__':
##    test_odd_calendar()
    test_normal_calendar()
