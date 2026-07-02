from django.contrib.auth.models import AbstractUser
from django.db import models

def get_avatar_path(instance, filename):
    return f'avatars/{instance.username}/{filename}'

class Profile(AbstractUser):
    avatar = models.ImageField(upload_to=get_avatar_path, blank=False, null=False)
    bio = models.TextField(max_length=500, blank=True, verbose_name="Информация о пользователе")
    phone_number = models.CharField(max_length=15, blank=True, verbose_name="Номер телефона")
    gender_choices = [ ('M', 'Мужской'), ('F', 'Женский'),('O', 'Другой')]
    gender = models.CharField(max_length=1, choices= gender_choices, blank=True, verbose_name="Пол")
    posts_count = models.IntegerField(default=0, verbose_name="Публикации")
    following_count = models.IntegerField(default=0, verbose_name="Подписки")
    followers_count = models.IntegerField(default=0, verbose_name="Подписчики")
    email = models.EmailField(unique=True, blank=False, null=False, verbose_name="Email")

    def __str__(self):
        return self.username + "'s Profile"

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'