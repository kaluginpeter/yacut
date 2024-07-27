Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/kaluginpeter/yacut
```

```
cd yacut
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```
Создайте файл .evn:
```
touch .evn
```

Создайте переменные:
```
FLASK_APP=yacut указывает, где находится flask приложение
FLASK_DEBUG=1 означает режим отладки, 0 означает запуск обычном режиме
DATABASE_URI='sqlite:///db.sqlite3' настройки базы данных
SECRET_KEY_FLASK_APP='1.618033988749' ключ для приложения flask
```

Команда для запуска:

```
flask run
```

### Справка по ручкам:

[![OpenApi](https://img.shields.io/badge/openapi-blue)](https://github.com/kaluginpeter/yacut/blob/master/openapi.yml)


### Stack of techonologies:
* Flask, Jinja2, SQL-Alchemy, Flask-WTF, Python

### Author:
* [Kalugin Peter Sergeevich](https://github.com/kaluginpeter)
