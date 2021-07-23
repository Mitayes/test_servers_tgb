-- https://postgrespro.ru/docs/postgresql/10/datatype-enum
-- Создаём тип перечисления для типа операционной системы
CREATE TYPE os_type AS ENUM ('Linux', 'Windows');
-- Создаём Таблицу, в которой будем хранить перечень серверов для тестирования
CREATE TABLE logs.server_list (
	server_name		text NOT null UNIQUE,	-- Доменное имя сервера
	server_ip		inet NOT null UNIQUE,	-- IP-адрес сервера
	server_alias	text NOT NULL,			-- Обезличенное название сервера (для анонимизации реального доменного имени сервера)
	server_type		os_type NOT null,		-- Тип сервера (Linux, Windows), необходимо для определения типа проверки (по порту ssh или RDP)
	server_note		text					-- Комментарий к серверу
);

-- Заливаем данные по серверам
INSERT INTO server_list VALUES 
	('localhost', '192.168.0.10', 'my_pc', 'Windows', ''),
	('server-postgreSQL', '192.168.0.21', 'PGSQL', 'Linux', '');
	

/* Создаём Связную Таблицу, в которой будем хранить логи тестирования серверов
Устанавливается связь с таблицей server_list по IP-адресу, изменение/удаление строк из главной таблицы никак не повлияет на связную */
CREATE TABLE logs.server_testing_logs (	
	server_ip			inet references logs.server_list (server_ip) on delete restrict on update restrict,	-- IP-адрес сервера
	server_ping_test	text not null,																		-- Результат тестирования методом ping
	server_rdp_test		text,																				-- Результат тестирования методом RDP
	server_ssh_test		text,																				-- Результат тестирования методом ssh
	date_testing		timestamp not null																	-- Дата и время тестирования
);
