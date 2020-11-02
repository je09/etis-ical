from datetime import datetime, date, timedelta
from string import digits
from bs4 import BeautifulSoup

WEEKDAY = {
        'Понедельник': 'mon',
        'Вторник': 'tue',
        'Среда': 'wed',
        'Четверг': 'thu',
        'Пятница': 'fri',
        'Суббота': 'sat',
    }

WEEKDAY_ID = {
        'mon': 1,
        'tue': 2,
        'wed': 3,
        'thu': 4,
        'fri': 5,
        'sat': 6,
    }

WEEKDAY_REVERSE = {
        'mon': 'Понедельник',
        'tue': 'Вторник',
        'wed' : 'Среда',
        'thu' : 'Четверг',
        'fri' : 'Пятница',
        'sat' : 'Суббота',
    }

MONTH = {
        'января': 1,
        'февраля': 2,
        'марта': 3,
        'апреля': 4,
        'мая': 5,
        'июня': 6,
        'июля': 7,
        'августа': 8,
        'сентября': 9,
        'октября': 10,
        'ноября': 11,
        'декабря': 12,
    }

MONTH_REVERSE = [None, 'января', 'февраля', 'марта',
                 'апреля', 'мая', 'июня', 'июля', 'августа',
                 'сентября', 'октября', 'ноября', 'декабря']


class Lesson:
    def __init__(self, lesson):
        self.time: [datetime] = []
        self.name: str = None
        self.auditory: str = None
        self.teacher: str = None

        self.parse_lesson(lesson)

    @staticmethod
    def parse_time(start_time, time_length=95):
        """
        Calculates end time of the lesson
        """

        start = datetime.strptime(start_time, '%H:%M')
        end = start + timedelta(minutes=time_length)

        return [start, end]

    def parse_lesson(self, lesson):
        lesson_meta = lesson.find_all('td')

        if lesson_meta[1].find('span', {'class': 'dis'}):  # Just in case
            self.time = self.parse_time(lesson_meta[0].font.text)

            self.teacher = lesson_meta[1].find('span', {'class': 'teacher'}).text.strip().split('\n')[0]
            self.name = lesson_meta[1].find('span', {'class': 'dis'}).text.strip()
            self.auditory = lesson_meta[1].find('span', {'class': 'aud'}).text


class Day:
    def __init__(self, day):
        self.date: date = None
        self.lessons: [Lesson] = []

        self.parse_day(day)

    @staticmethod
    def date_maker(date_title, year=datetime.now().year):
        """
        Converter from ETIS date to a serialized one
        """

        month = ''
        try:
            month = MONTH[(date_title.split(' ')[1])]
        except KeyError:
            print('Can\'t parse a month')
        day = int(date_title.split(' ')[0])

        return date(year, month, day)

    def parse_day(self, day):
        day_meta = day.h3.text.split(', ')  # Consists of <Day name>, date
        self.date = self.date_maker(day_meta[1])

        if not day.find('div', {'class': 'no_pairs'}):
            lessons_meta = day.table.find_all('tr')  # Dictionary of every lessons of the day
            for lesson in lessons_meta:
                self.lessons.append(Lesson(lesson))


class Week:
    days: [Day] = []

    def __init__(self, file_path):
        self.file_path = file_path
        self.html = self.__open_file__()

        self.parse_week()

    def __open_file__(self):
        with open(self.file_path, 'r', encoding='cp1251') as file:
            return ''.join(file.readlines())

    def parse_week(self):
        soup = BeautifulSoup(self.html, "lxml")
        timetable = soup.find_all('div', {'class': 'day'})

        for day in timetable:
            self.days.append(Day(day))




