import psycopg2
import datetime
import socket
import subprocess
from test_servers_config import *


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
	        logs.server_list.server_ip,
	        logs.server_list.server_type
        from logs.server_list
        ''')
    # Разбираем результат sql-запроса    
    for raw in cursor:
        server_param = {}
        # Заполняем словарь параметорв сервера
        server_param['server_ip'] = raw[0]
        server_param['server_type'] = raw[1]
        # Добавляем элемент в список серверов
        server_list.append(server_param)

    return server_list


def __test_servers__(server_ip_list):
    test_result = []
    for host in server_ip_list:
        print('start testimg:', host['server_ip'])
        # Определяем порт для тестирования
        if host['server_type'] == 'Windows':
            port = 3389
        elif host['server_type'] == 'Linux':
            port = 22
        
        # Запускаем тестирование методом ping
        ping_result = subprocess.Popen(["ping.exe", host['server_ip']],stdout = subprocess.PIPE, encoding='cp866').communicate()[0]
        # Определяем результат тестирования методом ping
        if ('TTL' in ping_result):
            result_ping = 'Ok'
        elif ('недоступен' in ping_result):
            result_ping = "Узел недоступен"
        elif ('Превышен интервал ожидания' in ping_result):
            result_ping = '100% потерь'
        elif ('не удалось обнаружить' in ping_result):
            result_ping = 'Узел не найден'
        else:
            result_ping = 'Не известная ошибка'

        # Запускаем тестирование методом rdp/ssh
        try:        
            conn_socket_test = socket.socket()
            conn_socket_test.connect((host['server_ip'], port))
            conn_socket_test.close()
            result_socket = 'Ok'
        except:
            result_socket = 'Error'        
        # Заполняем результаты тестирования методом rdp/ssh
        if port == 3389:
            result_rdp = result_socket
        else:
            result_rdp = 'undefined'
        if port == 22:
            result_ssh = result_socket
        else:
            result_ssh = 'undefined'            

        # Формируем данные для занесения в базу
        test_result.append((host['server_ip'], result_ping, result_rdp, result_ssh))

    return test_result


def __sql_insert_values__(test_result):
    for raw in test_result:
        # print(raw[0])
        cursor.execute(f'''
            INSERT INTO logs.server_testing_logs VALUES (
                '{raw[0]}',                 -- IP-адрес тестируемого сервера
                '{raw[1]}',                 -- результат тестирования ping
                '{raw[2]}',                 -- результат тестирования RDP
                '{raw[3]}',                 -- результат тестирования SSH
                '{datetime.datetime.now()}' -- Дата и время тестирования
                );
        ''')
    connector.commit()


if __name__ == '__main__':
    # Получаем список серверов с указанием типа сервера для тестирования
    server_list = __sql_get_server_list__(connector, cursor)
    # Запускаем тестирование серверов
    res = __test_servers__(server_list)
    # Заносим результаты тестирования в базу
    __sql_insert_values__(res)
    # Закрываем соединение с базой
    connector.close()
