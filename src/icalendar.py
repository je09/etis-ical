from datetime import datetime


class Calendar:
    calendar_head = ('BEGIN:VCALENDAR\n'\
    'VERSION:2.0\n'\
    'CALSCALE:GREGORIAN;\n'\
    'X-WR-CALNAME:{callname}\n'\
    'X-APPLE-LANGUAGE:ru\n'\
    'X-APPLE-REGION:RU\n'\
    'BEGIN:VTIMEZONE\n'\
    'TZID:Asia/Yekaterinburg\n'\
    'BEGIN:DAYLIGHT\n'\
    'TZOFFSETFROM:+0500\n'\
    'RRULE:FREQ=YEARLY;UNTIL=20100327T210000Z;BYMONTH=3;BYDAY=-1SU\n'\
    'DTSTART:19920329T020000\n'\
    'TZNAME:GMT+5\n'\
    'TZOFFSETTO:+0600\n'\
    'END:DAYLIGHT\n'\
    'BEGIN:STANDARD\n'\
    'TZOFFSETFROM:+0600\n'
    'DTSTART:20141026T020000\n'\
    'TZNAME:GMT+5\n'\
    'TZOFFSETTO:+0500\n'\
    'RDATE:20141026T020000\n'\
    'END:STANDARD\n'\
    'END:VTIMEZONE\n')
    event_body = ('BEGIN:VEVENT\n'\
    'CREATED:{create_datetime}Z\n'\
    'DTSTART;TZID=Asia/Yekaterinburg:{event_start_date}T{event_start_time}\n'\
    'DTEND;TZID=Asia/Yekaterinburg:{event_stop_date}T{event_stop_time}\n'\
    'TRANSP:OPAQUE\n'\
    'SUMMARY;LANGUAGE=ru:{event_name}\n'\
    'TRANSP:TRANSPARENT\n'\
    'VTIMEZONE\n'\
    # 'X-APPLE-UNIVERSAL-ID: 2008-05-02-03-23-05-63-@americanhistorycalendar.com\n'\
    'X-APPLE-TRAVEL-ADVISORY-BEHAVIOR:AUTOMATIC\n'\
    'SEQUENCE:0\n'\
    'LOCATION:{event_location}\n'\
    'DESCRIPTION:{event_description}\n'\
    'END:VEVENT\n')

    CALENDAR_END = 'END:VCALENDAR'

    def __init__(self):
        self._calendar_dictionary = {
            'calendar_name': None,
            'created': False,
        }

        self._event_list = []

    @staticmethod
    def _time_parser(_time):
        return '{:02d}{:02d}{:02d}'.format(_time.hour, _time.minute, _time.second)

    @staticmethod
    def _date_parser(_date):
        return '{:04d}{:02d}{:02d}'.format(_date.year, _date.month, _date.day)

    @staticmethod
    def _description_parser(_description):
        _output = ''
        if _description:
            _output = str(_description).strip('\n')

        return _output

    def create(self, calendar_name):
        if calendar_name:
            if not self._calendar_dictionary['created']:
                self._calendar_dictionary['calendar_name'] = calendar_name
                self._calendar_dictionary['created'] = True
            else:
                print('Calendar already created')
        else:
            print('No calendar name entered')

    def add(self, event_name, event_start_date, event_start_time, event_stop_date, event_stop_time, location=None, description=None):
        check_input = bool(
            str(event_name) + str(event_start_date) + str(event_start_time) +
            str(event_stop_date) + str(event_stop_date) + str(event_stop_time)
        )

        if check_input:
            if self._calendar_dictionary['created']:
                self._event_list.append({
                    'event_name': event_name,
                    'event_start_date': event_start_date,
                    'event_start_time': event_start_time,
                    'event_stop_date': event_stop_date,
                    'event_stop_time': event_stop_time,
                    'event_location': location,
                    'event_description': description,
                })
            else:
                print('Calendar is not created')
        else:
            print('Event name and datetime should not be empty')

    def remove(self, event_datetime):
        if event_datetime:
            if self._event_list:
                for event in self._event_list:
                    if event_datetime in event['event_datetime']:
                        self._event_list.remove(event)
            else:
                print('Event list is empty')
        else:
            print('Event name to remove should not be empty')

    def make(self):
        if self._calendar_dictionary['created']:
            ical_text = self.calendar_head.format(
                callname = self._calendar_dictionary['calendar_name']
            )

            create_datetime = datetime.now().strftime('%Y%m%dT%H%M%MT')

            if self._event_list:
                for event in self._event_list:
                    ical_text += self.event_body.format(
                        event_name=event['event_name'],
                        create_datetime=create_datetime,

                        event_start_date=self._date_parser(event['event_start_date']),
                        event_stop_date=self._date_parser(event['event_stop_date']),

                        event_start_time=self._time_parser(event['event_start_time']),
                        event_stop_time=self._time_parser(event['event_stop_time']),
                        event_location=event['event_location'].strip('\n'),
                        event_description=self._description_parser(event['event_description'])
                    )

            ical_text += self.CALENDAR_END

            return ical_text

        else:
            return False
