# EventsProj repo
Это репозиторий с кодом бекенд сервиса, который предоставляет пользователям:
*	Просматривать мероприятия,
*	Создавать мероприятия,
*	Регистрироватсья и принимать участие в мероприятиях.

## [Текущее состояние разработки](./doc/devstatus.md)

## Как работать в репе:
*	Создавать под фичи и задачи отдельные ветки
*	После завершения работы создавать ПР с указанием [меня](https://github.com/mvalkhimovich) для проверки
*	ПР просьба оформлять грамотно и, желательно, с указанием линки на карточку трелло (или как там оно)
*	ПР делаются в ветку dev
*	Ветка master существует для "релизных" версий

## Структура репозитория:
*	В app лежит код самого бекенда
*	В doc документация и картинки

## Используемые технологии:
*	Основа - [Python3](https://www.python.org/)
*	СУБД - [PostgreSQL](https://www.postgresql.org/)
*	Связь с БД - [SQLAlchemy](https://www.sqlalchemy.org/)
*	Web-framework - [Flask](http://flask.pocoo.org/)
*	Web-интерфейс - Временно(а может быть и нет `¯\_(ツ)_/¯`) [Bootstrap](https://getbootstrap.com/) 

## Установка:	
*	В первую очередь ставим нужные пакеты (Ubuntu):
		
		sudo apt install git python python3 python3-pip
		pip3 install virtualenv

*	Клонинуем репозиторий и настраиваем виртуальное окружение (bash/zsh):

		git clone git@github.com:EventsExpertsMIEM/EventsProj.git
		cd app
		python3 -m virtualenv venv
		. venv/bin/activate
	
*	Ставим зависимости проекта:

		pip3 install -r requirements.txt

*   Настраиваем PostgreSQL:
	-	Сама [настройка](./doc/db.md)
    -   Сервис берёт настройки БД через переменные окружения, поэтому рекомендуется использовать специальный скрипт (например [такой](./app/setup.sh)) и инициилизировать переменные окручения через `source setup.sh`
    -   Так же можно поднять PostgreSQL в облаке (например [Heroku](https://www.heroku.com/))

*   При первом запуске необходимо:
	-	указать опцию `--create-tables password`, чтобы в БД создались нужные табличкии
	-	password - пароль от учетной записи root_admin

*   Запуск происходит через `python3 main.py`
