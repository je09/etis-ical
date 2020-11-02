from datetime import datetime, date, timedelta
from string import digits

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


class Lesson:
    def __init__(self, time: [datetime], name: str, auditory: str, teacher: str):
        self.time = time
        self.name = name
        self.auditory = auditory
        self.teacher = teacher

    def end_time(start_time, time_length=95):
        """
        Calculates end time of the lesson
        """

        return datetime.strptime(start_time, '%H:%M') + timedelta(minutes=time_length)




class Day:
    def __init__(self, date_: datetime, lessons: [Lesson]):
        self.date = date_
        self.lessons = lessons


class WeekParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.html = self.__open_file__()

    def __open_file__(self):
        with open(self.file_path, 'r', encoding='cp1251') as file:
            return ''.join(file.readlines())



