from django.contrib.auth.models import AbstractUser
from django.db import models

def get_avatar_path(instance, filename):
    return f'avatars/{instance.username}/{filename}'
def get_post_path(instance, filename):
    return f'avatars/{instance.user.username}/posts/{filename}'

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
    subscriptions = models.ManyToManyField(
            'self',
            symmetrical=False,
            related_name='subscribers',
            blank=True,
            verbose_name="Подписки")

    def __str__(self):
        return self.username + "'s Profile"

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

class Post(models.Model):
    image = models.ImageField(upload_to=get_post_path, blank=False, null=False)
    description = models.TextField(max_length=300, blank= True, null= True, verbose_name="Описание")
    likes_count = models.IntegerField(default=0, verbose_name="Likes")
    comment_count = models.IntegerField(default=0, verbose_name="Комментарии")
    user = models.ForeignKey(Profile, on_delete=models.RESTRICT, blank=False, null=False, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")
    likes = models.ManyToManyField(Profile, related_name='liked_posts', blank=True, verbose_name="лайк")

    def __str__(self):
        return f'{self.pk} by {self.user.username}'
    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'
        ordering = ['-created_at']