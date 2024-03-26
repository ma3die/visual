from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager



class AccountManager(BaseUserManager):
    """
    Пользовательский Manager, где адрес email является уникальным
    идентификатором для аутентификации вместо username
    """

    def create_user(self, first_name, last_name, username, email, password=None):
        """
        Создаем и сохраняем Юзера
        """
        if not email:
            raise ValueError('У пользователя нет электронного адреса')
        if not username:
            raise ValueError('У пользователя нет имени пользователя')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            username=username
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, username, email, password=None):
        """
        Создаем и сохраняем суперюзера
        """
        if not email:
            raise ValueError('У пользователя нет электронного адреса')
        if not username:
            raise ValueError('У пользователя нет имени пользователя')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            username=username
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50, blank=True, verbose_name='Имя')
    last_name = models.CharField(max_length=50, blank=True, verbose_name='Фамилия')
    username = models.CharField(max_length=50, unique=True, verbose_name='Никнейм')
    email = models.EmailField(max_length=50, unique=True, verbose_name='Электронная почта')
    phone = models.CharField(max_length=50, blank=True, verbose_name='Телефон')
    birthday = models.DateTimeField(blank=True, null=True, verbose_name='День рождения')
    gender = models.CharField(max_length=10, blank=True, verbose_name='Пол')
    description = models.TextField(blank=True, verbose_name='О себе')
    url = models.CharField(blank=True, max_length=100, verbose_name='Cсылка на другие сайты')
    avatar = models.ImageField(upload_to='avatar/', blank=True, verbose_name='Аватарка',
                               validators=[FileExtensionValidator(
                                   allowed_extensions=('png', 'jpg', 'webp', 'jpeg', 'gif'))])
    subscription = models.CharField(max_length=10, blank=True,null=True, verbose_name='Подписка')
    date_register = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')
    last_join = models.DateTimeField(auto_now_add=True, verbose_name='Последний вход')
    is_admin = models.BooleanField(default=False, verbose_name='Администратор')
    is_active = models.BooleanField(default=False, verbose_name='Активный')
    is_staff = models.BooleanField(default=False, verbose_name='Персонал')
    is_superuser = models.BooleanField(default=False, verbose_name='Супер пользователь')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = AccountManager()

    def has_perms(self, perm, obj=None):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, package_name):
        return True

    class Meta:
        verbose_name = 'Учетная запись'
        verbose_name_plural = 'Учетные записи'



