# EventsProj repo
Это репозиторий с кодом бекенд сервиса, который предоставляет пользователям:
*	Просматривать мероприятия,
*	Создавать мероприятия,
*	Регистрироватсья и принимать участие в мероприятиях.


## Как работать в репе:
*	Создавать под фичи и задачи отдельные ветки
*	После завершения работы создавать ПР с указанием [меня](https://github.com/mvalkhimovich) для проверки
*	ПР просьба оформлять грамотно и, желательно, с указанием линки на карточку трелло (или как там оно)
*	ПР делаются в ветку dev
*	Ветка master существует для "релизных" версий

## Структура репозитория:
*	В app лежит код самого бекенда
	*	`core` - базовая логика
	*	`db` - структура и взаимодействие с бд
	*	`rest_cookie` - рестапи с cookies
	*	`rest_token` - рестапи с JWT
*	В doc документация и картинки
*	В extra скрипты

## Используемые технологии:
*	Основа - [Python3](https://www.python.org/)
*	СУБД - [PostgreSQL](https://www.postgresql.org/)
*	Связь с БД - [SQLAlchemy](https://www.sqlalchemy.org/)
*	Web-framework - [Flask](http://flask.pocoo.org/) 

## Установка:	
*	В первую очередь ставим нужные пакеты (Ubuntu):
		
		sudo apt install git python python3 python3-pip
		pip3 install virtualenv

*	Клонинуем репозиторий и настраиваем виртуальное (опционально для продакшн-сервера) окружение (bash/zsh):

		git clone git@github.com:EventsExpertsMIEM/EventsProj.git
		cd app
		python3 -m virtualenv venv
		. venv/bin/activate
	
*	Ставим зависимости проекта:

		pip3 install -r requirements.txt

*   Настраиваем PostgreSQL:
	-	Сама [настройка](./doc/db.md)
    -   Так же можно поднять PostgreSQL в облаке (например [Heroku](https://www.heroku.com/))


## Использование

*	Сервис берёт свои настройки (БД, параметры почты и др.) через переменные окружения, поэтому рекомендуется использовать специальный скрипт (например [такой](./extra/setup.sh) - рекомендуется положить заполненный вне папки репозиторя) и инициилизировать переменные окручения через `. setup.sh`/`source setup.sh`

*	Имеется два варианта запуска RESTapi - с cookies или JWT - отличия лишь в них. Для этого при запуске необходимо указать `rest_cookie` или `rest_token`.

*   При первом запуске необходимо указать `--create-tables password`, где первый параметр (пере)создает в БД нужные таблицы, а второй - пароль от начальной учетной записи `root_mail`

*   Запуск происходит через `python3 main.py` или же через `nohup python3 main.py > service.log &` если необходимо запустить сервис в фоне с записью логов в `service.log`