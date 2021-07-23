import psycopg2
from test_servers_config import *
from tgb_send_mess_pic import *


# Описываем подключение к базе (открываем соединение)
connector = psycopg2.connect(database=db_name, user=db_user,
                        password=db_passwd, host=db_ip, port=5432)
# Создаём курсор для общения с базой
cursor = connector.cursor()


# Функция для получения списка серверов (каждый элемент - это словарь со значениями ip-адрес и тип сервера)
def __sql_get_server_list__(connector, cursor):
    server_list = []
    cursor.execute(f'''
        select 
	        logs.server_list.server_ip
        from logs.server_list
        ''')
    # Разбираем результат sql-запроса    
    for raw in cursor:
        server_param = {}
        # Заполняем словарь параметорв сервера
        server_param['server_ip'] = raw[0]
        # server_param['server_type'] = raw[1]
        # Добавляем элемент в список серверов
        server_list.append(server_param)

    return server_list


def __sql_get_values__(server_list):
    # Сюда собираем результаты по всем серверам
    servers_status = []
    
    for server_ip in server_list:
        # Сюда собираем результаты по 1 серверу
        server_status = {}
        # Запускаем sql-скрипт для получения информации
        cursor.execute(f'''
            select 
            logs.server_testing_logs.server_ip,
            logs.server_list.server_alias,
            logs.server_list.server_type,
            logs.server_testing_logs.server_ping_test,
            logs.server_testing_logs.server_rdp_test,
            logs.server_testing_logs.server_ssh_test,
            logs.server_testing_logs.date_testing
        from logs.server_testing_logs, logs.server_list
        where 
            (logs.server_list.server_ip = logs.server_testing_logs.server_ip) and 
            (logs.server_testing_logs.server_ip = '{server_ip['server_ip']}') 
            order by logs.server_testing_logs.date_testing desc limit(1)
        ''')

        for raw in cursor:
            # Заливаем данные в словарь
            server_status['server_ip'] = raw[0]
            server_status['server_alias'] = raw[1]
            server_status['server_type'] = raw[2]
            server_status['ping_test'] = raw[3]
            server_status['rdp_test'] = raw[4]
            server_status['ssh_test'] = raw[5]
            server_status['date_test'] = raw[6].strftime('%Y-%m-%d %H:%m')
        
        servers_status.append(server_status)
    
    return servers_status


if __name__ == '__main__':
    # Получаем список серверов для тестирования
    server_list =  __sql_get_server_list__(connector, cursor)
    all_server_status = __sql_get_values__(server_list)

    tested_servers = []
    ping_err = []
    rdp_err = []
    ssh_err = []
    message = f'Результаты тестирования:\n'

    for server_status in all_server_status:
        tested_servers.append(server_status['server_alias'])
        # определяем проблемные сервера
        if server_status['ping_test'] == 'Ok':
            pass
        else:
            ping_err.append(server_status['server_alias'])
        
        if server_status['rdp_test'] == 'Error':
           rdp_err.append(server_status['server_alias']) 
        
        if server_status['ssh_test'] == 'Error':
            ssh_err.append(server_status['server_alias'])
    
    # Собираем сообщение для отправки   
    message += f'Протестированы сервера:\n{tested_servers}\n'
    if len(ping_err) > 0:
        message += f'Проблемы с доступностью по ping:\n{ping_err}'
    if len(rdp_err) > 0:
        message += f'Проблемы с доступностью по RDP:\n{rdp_err}'
    if len(ssh_err) > 0:
        message += f'Проблемы с доступностью по SSH:\n{ssh_err}'
    
    if (len(ping_err) == 0) and (len(rdp_err) == 0) and (len(ssh_err) == 0):
        message += 'Проблем не обнаружено'


# Для отправки сообщения в телеграм просто раскомментируем строку
# bot_send_message(message, chat_id)

print(message)

# Задача cron
# 0 */4 * * * USERNAME /usr/bin/python3 /home/pythonScripts/telegram_alarm/test_db_send_tgb.py
