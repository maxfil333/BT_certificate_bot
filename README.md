## Режим запуска
- если в корневой директории есть файл **DEBUG.json**:
```
config['save_dir'] = DEBUG.json..['save_dir']
config['TOKEN'] = DEBUG.json..['test_token']
```
- если нет:
```
save_dir = "...docs\CUSTOM\0 Документы с Районов\IN"
config['TOKEN'] = .env..['TOKEN']
```

## Для запуска бота на Windows Server:

1) Установить:

    - git
    - python 3.11.9

2) Клонировать репозиторий.
   <br>```git clone https://github.com/maxfil333/BT_certificate_bot.git ```

3) Создать в нем виртуальное окружение. Активировать его.
   <br>```python -m venv venv```
   <br>```venv\Scripts\activate```

4) Установить пакеты. Проверить.
   <br>```pip install -r requirements.txt```
   <br>```pip list```

5) Положить в корень проекта файл **env.env**
   или изменить в файле **src/config.py**
   <br>```load_dotenv(os.path.join(config['BASE_DIR'], 'env.env'))``` на <br>```load_dotenv(r"<путь_к_вашему_файлу_env>")```

6) При наличии базы данных добавить в корень проекта
   **config_files/database.db**

7) Выполнить (на выбор)
   - ```python main.py``` (если venv активировано)
   - или запустить ```run.bat``` (активация + запуск скрипта)