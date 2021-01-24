import requests


def parse_week(session_id, week_number):
    url = 'https://student.psu.ru/pls/stu_cus_et/stu.timetable?p_cons=y&p_week={week_number}'
    r = requests.get(url.format(week_number=week_number), cookies={'session_id': session_id})
    if '<form action="https://student.psu.ru/pls/stu_cus_et/stu.login" method="post" id="form">' in r.text:
        exit('Can\'t process request. Probably wrong session_id.')

    return r.text
