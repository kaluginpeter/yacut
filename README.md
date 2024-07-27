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

Команда для запуска:

```
flask run
```

### Справка по ручкам:
```
openapi.yml
```

### Stack of techonologies:
* Flask, Jinja2, SQL-Alchemy, Flask-WTF

### Author:
* [Kalugin Peter Sergeevich](https://github.com/kaluginpeter)
