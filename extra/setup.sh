#!/bin/bash

# пользователь postgresql
export PGUSER=""
# адрес postgresql
export PGHOST=""
# порт postgresql
export PGPORT=""
# название БД в postgresql
export PGDATABASE=""
# пароль пользователя postgresql
export PGPASSWORD=""

# порт приложения
export PORT=""

# метод авторизации - 'cookies' или 'tokens'
export AUTH_METHOD=""

# подтверждение регистрации по электронной почте
# 'active' для отключения подтверждения
# 'unconfirmed' для включения
export DEFAULT_USER_STATUS=""
# smtp сервер электронной почты
export SMTP_HOST=""
# адрес электронной почты для отправки
export MAIL_LOGIN=""
# пароль от электронной почты (рекомендуется создавать пароль приложения)
export MAIL_PASSWORD=""
# временно - линк на сервис (http(s)://адрес:порт)
export SITE_ADDR=""