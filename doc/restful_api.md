# EventsProj RESTful API

## Информация:
*   Принимает и отдаёт JSON

## Разработка [ВРЕМЕННО]:
*   Нет никакой авторизации - стреляй курлом как хочешь)
*   Всё равно ничего не сломаешь - онли регистрация, создание мероприятий и их список

## Описание:
*   `/login`  [POST]: [UNRELEASED]
    *    авторизация пользователя в системе
    *    принимает:
   	     *    `mail` [string] - почта пользователя
         *    `password` [string] - пароль пользователя
    *   успех:
         *    200 с `status: "ok"`
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

*   `/create_event`  [POST]:
    *   Создание мероприятия
    *   Принимает:
        *    `mail` [string] - почта создателя мероприятия
        *    `name` [string] - название мероприятия
        *    `sm_description` [string] - мелкое описание мероприятия (превью)
        *    `description` [string] - полное описание мероприятия
        *    `date` [string y-m-d-h-m] - дата проведения мероприятия
        *    `phone` [string] - телефон связи по мероприятию
        *    `presenters` [string, separator ',' или пустая строка] - перечисление почт докладчиков
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
             *    `date` [string y-m-d-h-m] - дата проведения мероприятия

*   `/join`  [POST]:
    *    регистрация пользователя на мероприятие
    *    принимает:
         *    `mail` [string] - почта пользователя
         *    `event_id` [string] - id мероприятия
    *   успех:
         *    200 с `status: "ok"` и `description: "Guest joined event"`
    *    неудача:
         *    400 с `error: DESCRIPTION`
