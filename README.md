### Что это?

Это генератор iCal из HTML-страницы с расписанием ЕТИС.
*Если вы не знаете, что такое ЕТИС – ваша жизнь намного проще, чем моя, я вам завидую.*

### Как использовать? 

Сначала нужно скачать и собрать этот скрипт использую команду
(Для этого у вас должен быть установлен Python 3)

```sh
git clone https://github.com/je09/etis-ical.git && cd etis-ical && pip install .
```

После чего, в терминале, вам станет доступна команда **etis**

Для генерации файла, нужно указать вашу группу и путь к файлу с расписанием, сделать это нужно так:

```sh
etis -g Группа -f /tmp/schedule.html
```

После конвертации .ics файл появится в папке, где лежала html страница (в данном случае в tmp)