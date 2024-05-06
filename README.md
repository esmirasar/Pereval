_______
# Pereval API
________
*Проект имеет спроектированную базу данных для объектов перевалов. 
Метод SubmitData принимает данные от пользователя и распределяет эти данные в подходящие таблицы в базе данных(пользователь, перевал, соординаты, уровень сложности, фотографии)*
____

**ФТСР** - Организация, занимающаяся развитием и популяризацией спортивного туризма в России и руководящая проведением всероссийских соревнования в этом виде спорта.

**Pereval API** - Компания ФТСР ведёт базу горных перевалов, которая пополняется туристами. Задача API максимально автоматизировать процесс добавления перевалов. Система требует изменения в виду отсутствия своевременной информации по перевалам.

**Задачи** 
> Во время проекта были поставлены задачи по разработке программного интерфейса приложения (API).
> Задачи разделились на 3 недели:
>  + 1 неделя - Изменение базы данных, и создание метода по приему данных от пользователя;
>  + 2 неделя - Создание методов по изменению и выводу информации, а также деплой проекта на хостинге;
>  + 3 неделя - Создание тестов и подготовка документации.
______
# Установка проекта
______
Необходимые команды для установки проекта
1. Клонирование проекта:
   > git clone https://github.com/esmirasar/Pereval;
3. Создание виртуального окружения:
   > python -m venv venv;
5. Установка библиотек проекта:
   > pip install -r req.txt;
7. Изменение переменных в настройках проекта(settings.py):
   ```python
   SECRET_KEY = os.getenv('SECRET_KEY')
   DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('NAME'),
        'HOST': os.getenv('HOST'),
        'PORT': os.getenv('PORT'),
        'USER': os.getenv('USER'),
      }
    }
   ```
8. Создание папку media в корневом каталоге проекта:

   *Директория media отвечает за загрузку image файлов перевала;*

9. Запуск тестов:
    + Для начала перейти в директорию с файлом
      > manage.py: cd pereval;
    + Запустить тесты:
      > python manage.py test;
     ________
### Далее нужно просто запустить проект:
 + Перейти в директорию с файлом
   > python manage.py: cd pereval
 + Запустить сервер:
   > python manage.py runserver
     
