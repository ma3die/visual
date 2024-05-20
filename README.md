# Социальная сеть Visual
### Описание
Проект представляет среднее между VK и Instagram в котором реализованы следующие возможности:
регистрация через email, VK, Google, редактирование личных данных, создание и редактирование постов,
комментирование постов и комментариев, подписки, онлайн чат, уведомления, онлайн оплата подписки через ЮКассу.

### Запуск проекта
...

## Архитектура приложения
### Технологии
Python 3.11, Channel 4.0.0, Daphne 4.1.0, Django 5.0.2, django-taggit 5.0.1, djangorestframework 3.14.0, python-magic 0.4.27, redis 5.0.2, yookassa 3.0.1, simplejwt 5.3.1

### Основные компоненты
Социальная сеть построена на базе фреймворков Django и Django REST Framework. Проект состоит
из 3 основных компонентов:
- База данных (СУБД PostgreSQL),
- NoSql база данных (Redis),
- visual.

# Описание социальной сети Visual
Состоит из 5 приложений:
- пользователи (accounts),
- онлайн чат (chat),
- подписчики (followers),
- уведомления notifications),
- посты (posts)

## Accounts
Приложение, которое отвечает за регистрацию, хранение и обработку пользователей, 
а также для оплаты подписок.

Список всех endpoint:

- POST /api/auth/reg/ Регистрация пользователей

&emsp;Запрос:
 ```
{
  "username": "string",
  "email": "user@example.com",
  "password": "string",
  "password2": "string"
}
  ```
&emsp;Ответ:
```
{
  "username": "string",
  "email": "user@example.com"
  "message": "Пользователь успешно создан"
}
  ```
&emsp;При попытке повторной регистрации ответ будет следующим:
  ```
{
   "email": ["Учетная запись с таким Электронная почта уже существует."]
}
  ```
- POST /api/auth/login/ Вход пользователя  

&emsp;Запрос:
```
{
  "email": "string",
  "password": "string"
}
```
&emsp;В ответе два токена: access и refresch:
```
{
  "access": "string",
  "refresh": "string"
}
```
- GET /api/auth/refresh_token/ Обновление токена  

&emsp;Запрос:
```
{
  "refresh": "string"
}
```
&emsp;Ответ:
```
{
  "access": "string"
}
```
- GET /api/auth/callback/ Вход пользователей через VK
- GET /api/auth/redirect/ Перенаправление пользователей регистрирующихся через VK
- GET /api/auth/callback_google/ Вход пользователей через Google
- GET /api/auth/redirect_google/ Перенаправление пользователей регистрирующихся через Google
- GET /api/confirm-email/{uidb64}/{token}/ Для подтверждения электронной почты 
- GET /api/me/ Получение данных о себе  

&emsp;Ответ:
```
{
  "id": 0,
  "last_login": "2024-05-14T11:22:44.678Z",
  "first_name": "string",
  "last_name": "string",
  "username": "string",
  "email": "user@example.com",
  "phone": "string",
  "birthday": "2024-05-14T11:22:44.678Z",
  "gender": "string",
  "description": "string",
  "url": "string",
  "avatar": "jpeg",
  "subscription": "string",
  "date_register": "2024-05-14T11:22:44.678Z",
  "last_join": "2024-05-14T11:22:44.678Z"
}
```
- PATCH /api/me/{id}/ Изменить свой профиль

&emsp;В строке запроса ввести свой id  

&emsp;Ответ:
```
{
  "last_login": "2024-05-14T11:24:24.147Z",
  "first_name": "string",
  "last_name": "string",
  "username": "string",
  "email": "user@example.com",
  "phone": "string",
  "birthday": "2024-05-14T11:24:24.147Z",
  "gender": "string",
  "description": "string",
  "url": "string",
  "avatar": "png",
  "subscription": "string"
}
```
- DELETE /api/me/delete/{id}/ Удалить свой профиль  

&emsp;В строке запроса ввести свой id  

- POST /api/create_payment/ Создание платежа для подписки  

&emsp;Запрос:  
&emsp;"subscription": 'normal' обычная подписка  
&emsp;"subscription": 'premium' премиум подписка
```
{
    "subscription": "string",
    "value": "int"
}
```
&emsp;Ответ:
```
{'confirmation_url': confirmation_url}
```
- POST /api/accepted_payment/ Для подтверждения оплаты подписки
- GET /api/users/ Получение всех пользователей  

&emsp;Ответ:
```
{
  "count": 123,
  "next": "http://api.example.org/accounts/?page=4",
  "previous": "http://api.example.org/accounts/?page=2",
  "results": [
    {
      "id": 0,
      "last_login": "2024-05-14T12:05:56.843Z",
      "first_name": "string",
      "last_name": "string",
      "username": "string",
      "email": "user@example.com",
      "phone": "string",
      "birthday": "2024-05-14T12:05:56.843Z",
      "gender": "string",
      "description": "string",
      "url": "string",
      "avatar": "png",
      "subscription": "string",
      "date_register": "2024-05-14T12:05:56.843Z",
      "last_join": "2024-05-14T12:05:56.843Z"
    }
  ]
}
```
- GET /api/users/{id}/ Получение конкретного пользователя

&emsp;В строке ввести id пользователя 
&emsp;Ответ:
```
{
  "id": 0,
  "last_login": "2024-05-14T12:07:47.352Z",
  "first_name": "string",
  "last_name": "string",
  "username": "string",
  "email": "user@example.com",
  "phone": "string",
  "birthday": "2024-05-14T12:07:47.352Z",
  "gender": "string",
  "description": "string",
  "url": "string",
  "avatar": "jpeg",
  "subscription": "string",
  "date_register": "2024-05-14T12:07:47.352Z",
  "last_join": "2024-05-14T12:07:47.352Z"
}
```
- PATCH /api/users/{id}/ Изменить данные пользователя (только админ)
- DELETE /api/users/{id}/ Удалить пользователя (только админ)
- GET /api/users/{id}/my_posts/ Получение всех постов пользователя  

&emsp;В строке ввести id пользователя 

&emsp;Ответ:
```
{
  "count": 123,
  "next": "http://api.example.org/accounts/?page=4",
  "previous": "http://api.example.org/accounts/?page=2",
  "results": [
    {
      "name": "string",
      "image": [
        {
          "id": 0,
          "image": "string",
          "post": 0
        }
      ],
      "video": [
        {
          "id": 0,
          "video": "string",
          "post": 0
        }
      ],
      "text": "string",
      "comments": [
        {
          "id": 0,
          "author": "string",
          "author_avatar": "string",
          "post": "string",
          "text": "string",
          "created_date": "2024-05-14T12:16:30.457Z",
          "update_date": "2024-05-14T12:16:30.457Z",
          "deleted": true,
          "lft": 0,
          "rght": 0,
          "tree_id": 0,
          "level": 0,
          "parent": 0,
          "notification": 0
        }
      ],
      "created_date": "2024-05-14T12:16:30.457Z",
      "slug": "string",
      "avialable_comment": true,
      "tags": [
        "string"
      ],
      "view_count": 2147483647,
      "author_id": 0,
      "author": "string",
      "is_like": true,
      "total_likes": "string",
      "likes": "string",
      "premium": true
    }
  ]
}
```
Модели:
- AccountManager (Пользовательский менеджер для регистрации через email),
- Account (Модель Аккаунта пользователя)

Представления:
- AccountViewSet (Получение пользователей),
- RegisterView (Регистрация пользователей),
- VKLoginRedirectView (Представление для перенаправления пользователей регистрирующихся через VK),
- VKLoginView (Представление для входа пользователей через VK),
- GoogleLoginRedirectView (Представление для перенаправления пользователей регистрирующихся через Google),
- GoogleLoginView (Представление для входа пользователей через Google),
- UserConfirmEmailView (Представление для подтверждения почты пользователя),
- ProfileViewSet (Получение и редактирование профиля пользователя),
- CreatePaymentView (Представление для оплаты подписки),
- CreatePaymentAcceptedView (Представление для проверки оплаты)

Сериализаторы:
- AccountSerializer (Сериализатор пользователей),
- RegisterSerializer (Сериализтор для регистрации пользователя),
- ProfileSerializer (Сериализатор профиля пользователей)

Ограничения доступа:
- IsAdminOrReadOnly (Только админ или только для чтения),
- IsOwnerOrReadOnly (Создатель поста или только для чтения),
- IsUserProfile (Пользователь профиля или только для чтения),
- IsAuthorComment (Создатель комментария или только для чтения),

Миксины:
- UserPostMixin (Миксин для получения личной страницы пользователя)

Сервисы:
- get_tokens_for_user (Получение токенов для пользователя), # в данный момент не используется
- my_post (Сервис для миксина UserPostMixin),
- random_string (Сервис для создания случайной строки),
- VKLoginCredentials (Сервис для данных входа в VK),
- vk_login_get_credentials (Сервис для получения данных входа в VK),
- VKLoginService (Сервис для обработки данных VK),
- GoogleLoginCredentials (Сервис для данных входа в VK),
- google_login_get_credentials (Сервис для получения данных входа в VK),
- GoogleAccessTokens (Сервис для расшифровки Google токенов),
- GoogleLoginService (Сервис для обработки данных VK)

  
## Chat
Live Chat. Написан с использованием Django Channels. Сам чат работает по WebSocket.

Список всех endpoint:  
- POST /api/conversations/start/ Старт чат

&emsp;Запрос:
  ```
  {
    "username": "string"
  }
  ```
&emsp;Варианты ответов:
  ```
  {
    "id": 1,
    "initiator": {
        "id": 2,
        "last_login": null,
        "first_name": "",
        "last_name": "",
        "username": "test_username2",
        "email": "test2@mail.ru",
        "phone": "",
        "birthday": null,
        "gender": "",
        "description": "",
        "url": "",
        "avatar": null,
        "subscription": null,
        "date_register": "2024-04-01T13:53:37.755981+03:00",
        "last_join": "2024-04-01T13:53:37.755981+03:00"
    },
    "receiver": {
        "id": 1,
        "last_login": null,
        "first_name": "Админ",
        "last_name": "Адимнов",
        "username": "admin",
        "email": "admin@mail.ru",
        "phone": "",
        "birthday": null,
        "gender": "",
        "description": "",
        "url": "",
        "avatar": null,
        "subscription": null,
        "date_register": "2024-04-01T13:45:26.704801+03:00",
        "last_join": "2024-04-01T13:45:26.704801+03:00"
    },
    "message_set": [],
    "start_time": "2024-05-14T15:36:25.651329+03:00"
}
  ```
  ```
  {'message': 'Получатель не найден'}
  ```
&emsp;Если чат уже создан, перенеправление на него с номером id:

- GET /api/conversations/{convo_id}/ Если чат уже создан  
В строке запроса передается id чата  
&emsp;Варианты ответов:
  ```
  {
    "id": 1,
    "initiator": {
        "id": 2,
        "last_login": null,
        "first_name": "",
        "last_name": "",
        "username": "test_username2",
        "email": "test2@mail.ru",
        "phone": "",
        "birthday": null,
        "gender": "",
        "description": "",
        "url": "",
        "avatar": null,
        "subscription": null,
        "date_register": "2024-04-01T13:53:37.755981+03:00",
        "last_join": "2024-04-01T13:53:37.755981+03:00"
    },
    "receiver": {
        "id": 1,
        "last_login": null,
        "first_name": "Админ",
        "last_name": "Адимнов",
        "username": "admin",
        "email": "admin@mail.ru",
        "phone": "",
        "birthday": null,
        "gender": "",
        "description": "",
        "url": "",
        "avatar": null,
        "subscription": null,
        "date_register": "2024-04-01T13:45:26.704801+03:00",
        "last_join": "2024-04-01T13:45:26.704801+03:00"
    },
    "message_set": [],
    "start_time": "2024-05-14T15:36:25.651329+03:00"
  }
  ```
  ```
  {
    "message": "Чат не найден"
  }
  ```
- GET /api/conversations/ Список всех чатов пользователя 
с выводом последнего сообщения в каждом чате. 

&emsp;Ответ:
  ```
  [
    {
        "initiator": {
            "id": 2,
            "last_login": null,
            "first_name": "",
            "last_name": "",
            "username": "test_username2",
            "email": "test2@mail.ru",
            "phone": "",
            "birthday": null,
            "gender": "",
            "description": "",
            "url": "",
            "avatar": null,
            "subscription": null,
            "date_register": "2024-04-01T13:53:37.755981+03:00",
            "last_join": "2024-04-01T13:53:37.755981+03:00"
        },
        "receiver": {
            "id": 1,
            "last_login": null,
            "first_name": "Админ",
            "last_name": "Адимнов",
            "username": "admin",
            "email": "admin@mail.ru",
            "phone": "",
            "birthday": null,
            "gender": "",
            "description": "",
            "url": "",
            "avatar": null,
            "subscription": null,
            "date_register": "2024-04-01T13:45:26.704801+03:00",
            "last_join": "2024-04-01T13:45:26.704801+03:00"
        },
        "last_message": {
            "text": "",
            "attachment": null,
            "read": false,
            "sender": null,
            "receiver": null
        }
    }
  ]
  ```
WebSocket:  
- ws/chat/(?P<room_name>\w+)/$ Live chat   
  Передаем номер чата и access токен в строке.
- ws/notifications/ Для получения уведомлений  

Модели:
- Conversation (Модель чата)
- Message (Модель сообщения)  

Представления:
- start_convo (Старт чата)
- get_conversation (Получение конкретного чата)
- conversations (Получение всех чатов пользователя)

Сериализаторы:
- MessageSerializer (Сериайлазер сообщений)
- ConversationListSerializer (Сериалайзер для вывода всех чатов)
- ConversationSerializer (Сериалайзер чата)

Потребители (Consumers):
- ChatConsumer (Чат между пользователями)
- NotificationConsumer (Создание уведомлений о сообщении)

Middleware:
- JwtAuthMiddleware (Middleware авторизации)
- get_user (Получение пользователя)


## Followers
Приложение для работы с подписками.

Список всех endpoint:  
- POST /api/subscribe/ Подписаться на пользователя. Если уже подписан - отписаться

&emsp;Запрос:
```
{
  "author": 0,
  "follower": 0
}
```
&emsp;Ответ:
```
{
  "author": 0,
  "follower": 0
}
```
- GET /api/my_followers/{author_id}/ Подписчики пользователя  

&emsp;В запросе передать id автора  
&emsp;Ответ:
```
{
  "author": 0,
  "follower": 0
}
```
- GET /api/my_subscriptions/{follower_id}/ Подписки пользователя

&emsp;В запросе передать id пользователя  
&emsp;Ответ:
```
{
  "author": 0,
  "follower": 0
}
```

Модели:
- Follower (Модель подписчиков)

Представления:
- FollowerViewSet (Подписаться, отписаться, посмотреть подписки и подписчиков)

Сериализаторы:
- FollowerSerializer (Сериалайзер подписки и отписки от юзера)


## Notifications
Приложение отвечает за уведомления.

Список всех endpoint:  
- GET /api/notifications/ Количество всех уведомлений пользователя  

&emsp;Ответ:
```
{'count_notification': 'int'}
```
- GET /api/notifications/push/ Точка которую пингует фронт для получения новых уведомлений

&emsp;Варианты ответов:
```
{'count_notification': 'int'}
```
```
{'message': 'Новых уведомлений нет'}
```
- GET /api/notifications/list/ Выводит все уведомления

&emsp;Варианты ответов:
```
{
  "count": 123,
  "next": "http://api.example.org/accounts/?page=4",
  "previous": "http://api.example.org/accounts/?page=2",
  "results": [
    {
      "id": 0,
      "user": {
        "id": 0,
        "last_login": "2024-05-14T13:50:08.978Z",
        "first_name": "string",
        "last_name": "string",
        "username": "string",
        "email": "user@example.com",
        "phone": "string",
        "birthday": "2024-05-14T13:50:08.978Z",
        "gender": "string",
        "description": "string",
        "url": "string",
        "avatar": "gif",
        "subscription": "string",
        "date_register": "2024-05-14T13:50:08.978Z",
        "last_join": "2024-05-14T13:50:08.978Z"
      },
      "send": true,
      "read": true,
      "hide": true,
      "created_date": "2024-05-14T13:50:08.978Z"
    }
  ]
}
```
```
{'message': 'Новых уведомлений нет'}
```

Модели:
- Notification (Модель для уведомлений)

Представления:
- NotificationView (Получаем количество уведомления, точка для пинга, список всех уведомлений)

Сериализаторы:
- CreateSerializerNotification (Сериалайзер для уведомлений)


## Posts
Приложение отвечает за создание, редактирование, удаление постов. Также реализована система
комментариев и лайков.

Список всех endpoint:  
- GET /api/posts/ Выводит все посты  

&emsp;Ответ:
```
{
  "count": 123,
  "next": "http://api.example.org/accounts/?page=4",
  "previous": "http://api.example.org/accounts/?page=2",
  "results": [
    {
      "name": "string",
      "image": [
        {
          "id": 0,
          "image": "string",
          "post": 0
        }
      ],
      "video": [
        {
          "id": 0,
          "video": "string",
          "post": 0
        }
      ],
      "text": "string",
      "comments": [
        {
          "id": 0,
          "author": "string",
          "author_avatar": "string",
          "post": "string",
          "text": "string",
          "created_date": "2024-05-20T13:13:52.409Z",
          "update_date": "2024-05-20T13:13:52.409Z",
          "deleted": true,
          "lft": 0,
          "rght": 0,
          "tree_id": 0,
          "level": 0,
          "parent": 0,
          "notification": 0
        }
      ],
      "created_date": "2024-05-20T13:13:52.409Z",
      "slug": "string",
      "avialable_comment": true,
      "tags": [
        "string"
      ],
      "view_count": 2147483647,
      "author_id": 0,
      "author": "string",
      "is_like": true,
      "total_likes": "string",
      "likes": "string",
      "premium": true
    }
  ]
}
```
- POST /api/posts/ Создание поста

&emsp;Запрос:  
&emsp;Например в Postman делается через form-data.  
&emsp;name - название поста  
&emsp;tags[0] - первый тэг  
&emsp;tags[1] - второй тэг  
&emsp;image - картинка
&emsp;video - видеофайл

&emsp;Ответ:  
```
{
  "name": "string",
  "image": [
    {
      "image": "string",
      "post": 0
    }
  ],
  "video": [
    {
      "video": "string",
      "post": 0
    }
  ],
  "text": "string",
  "avialable_comment": true,
  "tags": [
    "string"
  ],
  "view_count": 2147483647,
  "author": "string"
}
```
- GET /api/posts/{slug}/ Получение поста по слагу

&emsp;Ответ:  
```
{
  "name": "string",
  "image": [
    {
      "id": 0,
      "image": "string",
      "post": 0
    }
  ],
  "video": [
    {
      "id": 0,
      "video": "string",
      "post": 0
    }
  ],
  "text": "string",
  "comments": [
    {
      "id": 0,
      "author": "string",
      "author_avatar": "string",
      "post": "string",
      "text": "string",
      "created_date": "2024-05-20T13:40:05.491Z",
      "update_date": "2024-05-20T13:40:05.491Z",
      "deleted": true,
      "lft": 0,
      "rght": 0,
      "tree_id": 0,
      "level": 0,
      "parent": 0,
      "notification": 0
    }
  ],
  "created_date": "2024-05-20T13:40:05.491Z",
  "slug": "string",
  "avialable_comment": true,
  "tags": [
    "string"
  ],
  "view_count": 2147483647,
  "author_id": 0,
  "author": "string",
  "is_like": true,
  "total_likes": "string",
  "likes": "string",
  "premium": true
}
```
- PUT /api/posts/{slug}/ Изменение поста по слагу
- PATCH /api/posts/{slug}/ Изменение поста по слагу
- DELETE /api/posts/{slug}/ Удаление поста по слагу
- POST /api/posts/{slug}/like/ Лайк поста по слагу
- GET /api/posts/{slug}/likes/ Получение профилей кто лайкнул пост
- POST /api/posts/{slug}/unlike/ Убрать лайк с поста
- GET /api/search/ Поиск через Postgre
- POST /api/comments/ Создание комментария к посту  

&emsp;Запрос:   
&emsp;post - slug поста  
&emsp;parent - id комментария. Для ответа на комментарий - вставляем его id.
```
{
  "post": "string",
  "text": "string",
  "parent": 0
}
```

- PUT /api/comments/{id}/ Изменить комментарий
- PATCH /api/comments/{id}/ Изменить комментарий
- DELETE /api/comments/{id}/ Удалить комментарий

Модели:
- Like (Модель для лайков)
- Post (Модель поста)
- Image (Галерея фотографий)
- Video (Галерея видео)
- Comment (Модель для комментариев)
- ReadPost (Модель просмотра статей)

Представления:
- PostViewSet (Представление CRUD для постов)
- CommentView (Представление CRUD для комментариев)
- SearchResultView (Поиск с помощью Postgre)

Сериализатры:
- FilterCommentListSerializer (Фильтр комментариев, только parents)
- RecursiveSerializer (Вывод рекурсивно children)
- LikeSerializer (Лайки)
- ImageSerializer (Картинки)
- VideoSerializer (Видео)
- CommentSerializer (Комментарии)
- ListPostSerializer (Список статей)
- PostSerializer (Пост)
- CreateCommentSerializer (CRUD комментариев)

Миксины:
- LikedMixin (Поставить, удалить просмотреть лайки)
- AddImageVideoMixin(Миксин для выбора типа файла и записи в модель)

Сервисы:
- add_like (Добавить лайк)
- remove_like (Удалить лайк)
- is_like (Проверка лайкнул ли юзер пост)
- get_likes (Получаем всех пользователей, которые лайкнули пост)

Утилиты:
- get_mime_typ (Функция для проверки типа фаула)
- unique_slugify (Генератор уникальных SLUG для моделей)