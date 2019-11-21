# EventsProj Database

## Почему PostgreSQL
* Хорошая докумантция и большое сообщество.
* Поддержка множества дополнительных типов, например UUID, JSONB и другие.
* Следует ACID (в отличии от MySQL/InnoDB).
* Шардирование из коробки.

Но в то же время проигрывает MySQL по скорости работы.

## Как поставить PostgreSQL (Ubuntu)
1) Ставим пакет:

		sudo apt install -y postgresql

2) Переходим в суперюзера бд:

		sudo su - postgres

3) Заводим новую роль:

		createuser %usename% --pwprompt

4) Заводим саму БД:

		createdb -O %username% %dbname%

5) Подключаемся к новой БД и даем доступы:

		psql %dbname% 
		GRANT ALL ON DATABASE %dbname% to %username%;

После этого можно подключиться к БД задав нужные переменные окружения из `setup.sh` и набрав в консоли `psql`.
