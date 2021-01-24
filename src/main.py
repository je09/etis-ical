from pathlib import Path

import click

from src.parser import Week
from src.icalendar import Calendar
from src.etis_requests import parse_week

VERSION = 1.0


def print_version(ctx, _, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo('etis-ical version {0}'.format(VERSION))
    ctx.exit()


@click.command()
@click.option(
    '-g',
    '--group',
    prompt='Input group name',
    type=str,
    help='--group ИТХ'
)
@click.option(
    '-f',
    '--file_path',
    type=str,
    help='Required file should be saved from https://student.psu.ru/pls/stu_cus_et/stu.timetable \n'
         'You have to provide a path of the HTML-code you saved from the link above\n'
         '--file_path /tmp/schedule.html\n'
         'The result\'ll be saved in the same folder.'
)
@click.option(
    '-s',
    '--session',
    type=str,
    help='You can obtain ETIS session id after authorizing by pasting "console.log(document.cookie)" into the '
         'web console of your browser.'
)
@click.option(
    '-w',
    '--week_number',
    type=str,
    help='Number of week to parse automatically.'
)
@click.option(
    '-v',
    '--version',
    is_flag=True,
    callback=print_version,
    expose_value=False,
    is_eager=True,
    help='Show version of the haruhi-script'
)
def main(group, file_path, session, week_number):
    if not file_path and not session:
        exit('You must provide file path or session id')

    if session and not week_number:
        exit('The number of week to parse must be provided')

    if file_path:
        path = Path(file_path)
        week = file_read(path)

    if session:
        path = Path(f'{week_number}.ics')
        week = Week(parse_week(session, week_number))

    ical = generate_ical(week, group)



    click.echo('Saving iCal file')
    ical_path = '{}/{}.ics'.format(path.parent, path.stem)

    with open(ical_path, 'w') as file:
        file.writelines(ical)

    click.echo('iCal file saved at {}'.format(ical_path))


def file_read(path):
    if not path.is_file():
        exit('Provided file doesn\'t exist or it\'s not a file')

    click.echo('Parsing file')
    with open(path.absolute(), 'r', encoding='cp1251') as file:
        week = Week(''.join(file.readlines()))

    if not week.days:
        exit('Provided file is invalid')

    return week


def generate_ical(week, group):
    click.echo('Generating iCal file')
    cal = Calendar()
    cal.create(group)

    for day in week.days:
        for lesson in day.lessons:
            if lesson.name:
                cal.add(
                    event_name=lesson.name,
                    event_start_time=lesson.time[0],
                    event_stop_time=lesson.time[1],
                    event_start_date=day.date,
                    event_stop_date=day.date,
                    location=lesson.auditory,
                    description=lesson.teacher
                )

    return cal.make()


if __name__ == '__main__':
    main()
