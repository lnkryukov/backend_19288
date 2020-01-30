# 19288 Evetns Project RESTful API

## Информация:
*   Принимает и отдаёт JSON

## Описание:
*   `/login`  [POST]:
    *    авторизация пользователя в системе
    *    принимает:
   	     *    `mail` [string] - почта пользователя
         *    `password` [string] - пароль пользователя
    *    успех:
         *    200 с `status: "ok"`
    *    неудача:
         *    400 с `error: DESCRIPTION`

*   `/logout`  [GET/POST]:
    *    Логаут пользователя из системы
    *    успех:
         *    200 с `status: "ok"` и `description: "User was logouted"`
    *    неудача:
         *    400 с `error: DESCRIPTION`

*   `/register`  [POST]:
    *    регистрация пользователя в системе
    *    принимает:
         *    `mail` [string] - почта пользователя
         *    `name` [string] - имя пользователя
         *    `surname` [string] - фамилия пользователя
         *    `password` [string] - пароль пользователя
    *   успех:
         *    200 с `status: "ok"`
    *    неудача:
         *    400 с `error: DESCRIPTION`

*   `/register`  [POST]:
    *    регистрация пользователя в системе
    *    принимает:
         *    `link` [string] - ссылка подтверждения пользователя
    *    успех:
         *    200 с `status: "ok"` и `description: "User was confirmed"`
    *    неудача:
         *    400 с `error: DESCRIPTION`

*   `/create_event`  [POST]:
    *   Создание мероприятия
    *   Принимает:
        *    `name` [string] - название мероприятия
        *    `sm_description` [string] - мелкое описание мероприятия (превью)
        *    `description` [string] - полное описание мероприятия
        *    `date` [string yyyy-mm-ddThh:mm] - дата проведения мероприятия
    *   Успех:
        *    200 с:
             *    `status` - `"ok"`
             *    `description` - `"Event was created!"`
             *    `params` - `ID_EVENT` [unsigned int] - id созданного мероприятия
    *    неудача:
         *    400 с `error: DESCRIPTION`

*   `/events`  [GET]:
    *   Получение списка всех мероприятий
    *   отдаёт:
        *   пары `id` [unsigned int] : `данные по мероприятию`, где данные имеют вид:
             *    `id` [unsigned int] - id мероприятия
             *    `name` [string] - название мероприятия
             *    `sm_description` [string] - мелкое описание мероприятия (превью)
             *    `date_time` [string yyyy-mm-ddThh:mm] - дата проведения мероприятия
    *   в случе проблем:
        *    400 с `error: DESCRIPTION`

*   `/join`  [POST]:
    *    регистрация пользователя на мероприятие
    *    принимает:
         *    `event_id` [string] - id мероприятия
         *    `role` [string] - роль присоединившегося (`presenter` или `participant`)
    *    успех:
         *    200 с `status: "ok"` и `description: "Guest joined event"`
    *    неудача:
         *    400 с `error: DESCRIPTION`

*   `/event/<int:id>`  [GET]:
    *   Получение информации о мероприятии
    *   отдаёт:
        *    `creator_mail` [string] - почта создателя мероприятия
        *    `phone` [string] - телефон создателя мероприятия
        *    `name` [string] - название мероприятия
        *    `sm_description` [string] - мелкое описание мероприятия (превью)
        *    `description` [string] - полное описание мероприятия
        *    `date_time` [string yyyy-mm-dd-hh-mm] - дата проведения мероприятия
    *   в случе проблем:
        *    400 с `error: DESCRIPTION`

*   `/profile`  [GET]:
    *   Получение информации о пользователе и его мероприятиях
    *   отдаёт:
        *   `creator` : список мероприятий, где данный пользователей создатель
        *   `presenter` : список мероприятий, где данный пользователей докладчик
        *   `guest` : список мероприятий, где данный пользователей гость
        *   каждое мероприятие выглядит как пара `id` : `данные по мероприятию`, где данные имеют вид:
            *    `id` [int] - id мероприятия
            *    `name` [string] - название мероприятия
            *    `date_time` [string yyyy-mm-dd-hh-mm] - дата проведения мероприятия
    *   в случе проблем:
        *    400 с `error: DESCRIPTION`
