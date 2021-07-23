# test_servers_tgb
Тестирование серверов и уведомление в телеграм (хранение данных в БД)

## Используемые модули
* psycopg2
* datetime
* socket
* subprocess
* БД PostgreSQL

## Описание файлов

### ![test_servers_config.py](https://github.com/Mitayes/test_servers_tgb/blob/main/test_servers_config.py)
Конфигурационный файл, содержащий секреты (лучше использовать переменные окружения)

### ![test_servers_postgres.sql](https://github.com/Mitayes/test_servers_tgb/blob/main/test_servers_postgres.sql)
SQL-запросы для создания таблиц:
* Таблица-справочник, описывающая сервера
* Таблица в которой аккумулируются логи тестирования.  

Таблицы создавались в схеме `logs`

### ![tgb_send_mess_pic.py](https://github.com/Mitayes/test_servers_tgb/blob/main/tgb_send_mess_pic.py)
Описывает функции, с помощью которых можно отправить сообщение в канал телеграм (`bot_send_message`), и изображение (`bot_send_photo`). Данные функции импортируются в `test_servers_send_info_tgb.py`

### ![test_servers_config.py](https://github.com/Mitayes/test_servers_tgb/blob/main/test_servers_db.py)
Используется для тестирования доступности серверов методом ping, попытки установить соединение по RDP порту 3389, а также попытки установить соединение по SSH порту 22  
Тестирование по RDP игнорируется, если тип сервера в БД Linux  
Тестирование по SSH игнорируется, если тип сервера в БД Windows  
  
**ping реализован посредством вызова внешней команды** ping.exe (т.е. в данном случае работает только при запуске скрипта под Windows)  

### ![test_servers_send_info_tgb.py](https://github.com/Mitayes/test_servers_tgb/blob/main/test_servers_send_info_tgb.py)
Извлекает последние результаты тестирования из БД, формирует сообщение о результате тестирования. Также может отправить сообщение с результатом тестирования в канал Телеграм  

