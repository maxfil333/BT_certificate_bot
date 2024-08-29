## Для запуска бота на Windows Server:
1) Установить:
- git
- python 3.11.9 

2) Клонировать репозиторий.
```git clone https://github.com/maxfil333/BT_certificate_bot.git ```

3) Создать в нем виртуальное окружение. Активировать его.
	```python -m venv venv```
	```venv\Scripts\activate```

4) Установить пакеты. Проверить.
	```pip install -r requirements.txt```
	```pip list```
	
5) Положить в корень проекта файл **.env**
   или изменить в файле **src/config.py**
   ```load_dotenv()``` на ```load_dotenv(r"<путь_к_вашему_файлу_env>")```

6) При наличии базы данных добавить в корень проекта
**config_files/database.db**

7) При активированном окружении (venv) выполнить
	```python main.py```