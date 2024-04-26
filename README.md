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
Приложение которое отвечает за регистрацию, хранение и обработку пользователей.

Список всех endpoint:

- POST /api/auth/login/
- POST /api/auth/reg/
- GET /api/auth/callback/
- GET /api/auth/redirect/
- GET /api/auth/callback_google/
- GET /api/auth/redirect_google/
- GET /api/auth/refresh_token/
- GET /api/confirm-email/{uidb64}/{token}/
- GET /api/me/
- PATCH /api/me/{id}/
- DELETE /api/me/delete/{id}/
- POST /api/create_payment/
- POST /api/accepted_payment/
- GET /api/users/
- POST /api/users/
- GET /api/users/{id}/
- PUT /api/users/{id}/
- PATCH /api/users/{id}/
- DELETE /api/users/{id}/
- GET /api/users/{id}/my_posts/

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

### Описание работы:
- Регистрация пользователей.
  Для регистрации пользователей используется точка ```/api/auth/reg/```.
  Запрос:
  ```
  {
  "username": "string",
  "email": "user@example.com",
  "password": "string",
  "password2": "string"
  }
  ```
  При регистрации используется представление RegisterView, в котором определен сериалайзер RegisterSerializer и в нем метод create, который шифрует пароль, устанавливает атрибут is_active  в True и сохраняет пользователя в базу.  
  Ответ:
  ```
  {
  "username": "string",
  "email": "user@example.com"
  "message": "Пользователь успешно создан"
  }
  ```
  При попытке повторной регистрации ответ будет следующим:
  ```
  {
    "email": ["Учетная запись с таким Электронная почта уже существует."]
  }
  ```
  Как писалось выше, некоторый функционал еще на стадии разработки. Поэтому для отправки письма для подтверждения электронной почты
  необходимо в файле seriaziers.py убрать комментарии на строках 46-56 и в строке 43 ```user.is_active = True``` исправить на False.
  Теперь пр попытке регистрации, в сериалайзере RegisterSerializer генерируется токен ```token = default_token_generator.make_token(user)``` используя объект User. Этот токен используется для создания URL-адреса активации.
  Для кодирования индентификатора пользователя используется функция ```urlsafe_base64_encode```, а затем этот идентификатор и токен используются в ```reverse_lazy()``` для создания URL-адреса активации.
  Далее текущий домен сайта получается с помощью ```Site.objects.get_current().domain```.
  
