# Описание.
## _Финальный проект 9 спринта_

Проект закрепляет знания, полученные в теории 8 и 9 спринтов

- выполнение запросов к API
- получение, добавление данных через API = 
- ✨Magic ✨

## Установка

- Клонировать на свой АРМ репозиторий
- активировать настройки, загрузить требуемые пакеты - в bash git - pip install -r requirements.txt
- для ОС Windows из консоли или bash git запустить проект - python manage.py runserver
- для ОС RHEL из консоли или bash git запустить проект - python3 manage.py runserver
-подразумевается что python установлен на АРМ

Перед запуском проекта нужно убедиться в наличии установленной последней версии pip - в bash git - ....
Оф. сайт git - [https://git-scm.com/downloads] оф. сайт python -  [https://www.python.org/][df1]



## Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

git clone https://github.com/.........

cd ....

Cоздать и активировать виртуальное окружение (VSC, Win):

python -m venv env

source env/bin/activate

Установить зависимости из файла requirements.txt (MacOs, RHEL):

python3 -m pip install --upgrade pip
pip install -r requirements.txt

Установить зависимости из файла requirements.txt (Win):

python -m pip install --upgrade pip
pip install -r requirements.txt

Выполнить миграции (MacOs, RHEL):

python3 manage.py migrate

Выполнить миграции (Win):

python manage.py migrate

Запустить проект (MacOs, RHEL):

python3 manage.py runserver

Запустить проект (Win):

python manage.py runserver