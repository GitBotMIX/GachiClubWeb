from django.db import models
import datetime
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models import Sum, Count


class Gifts(models.Model):
    name = models.CharField(max_length=80, db_index=True, verbose_name='Название')
    description = models.CharField(max_length=200, db_index=True, verbose_name='Описание')
    blocked_until = models.DateTimeField(verbose_name='Заблокировано до')
    complete_until = models.DateTimeField(verbose_name='Завершиться', null=True)
    image = models.ImageField(upload_to='gift_image/%Y/%m/%d', blank=True, verbose_name='Картинка')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Призы'
        verbose_name_plural = 'Призы'

    def __str__(self):
        return self.name

    def unblocked(self):
        if timezone.now() >= self.blocked_until:
            return True
        else:
            return False

    def unblocked_via(self):
        return int((self.blocked_until - timezone.now()).total_seconds())

    def dont_complete(self):
        return timezone.now() >= self.complete_until


class Category(models.Model):
    name = models.CharField(max_length=30, db_index=True, verbose_name='Название')
    color = models.CharField(max_length=30, db_index=True, verbose_name='Цвет(HEX)', default='#ffffff')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Quests(models.Model):
    category = models.ForeignKey(Category, related_name='Категория', on_delete=models.CASCADE)
    title = models.CharField(max_length=60, db_index=True, verbose_name='Заголовок')
    description = models.TextField(blank=True, verbose_name='Описание')
    reward = models.SmallIntegerField(verbose_name='Награда')
    DIFFICULTIES = (
        (0, 'Low'),
        (1, 'Normal'),
        (2, 'High'),
    )
    complexity = models.SmallIntegerField(verbose_name='Сложность', default=0, choices=DIFFICULTIES)
    amount_available_user = models.SmallIntegerField(verbose_name='Количество доступное для пользователя', default=1)
    available = models.BooleanField(default=True, verbose_name='Активность')

    objects = models.Manager()
    completed_count = models.Manager()

    class Meta:
        ordering = ('reward',)
        verbose_name = 'Задание'
        verbose_name_plural = 'Задания'

    def __str__(self):
        return self.title

    def completed_count(self, user, quest):
        return UserQuests.objects.filter(user=user, quest_completed=quest).aggregate(completed_count=Count('id'))['completed_count']


class UserQuests(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    completed_at = models.DateTimeField(auto_now_add=True, verbose_name='Выполнено')
    quest_completed = models.ForeignKey(Quests, on_delete=models.CASCADE, verbose_name='Выполненное задание',
                                        blank=True)

    class Meta:
        verbose_name = 'Выполненные задания'
        verbose_name_plural = 'Выполненное задание'

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}; {self.quest_completed};' \
               f' {self.completed_at}'


class UserProfileManager(models.Manager):
    def add_points(self, user, points):
        if '-' in points:
            points = points.replace('-', '')
            return self.remove_points(user, points)
        user_profile = self.get(user=user)
        user_profile.points += int(points)
        user_profile.save()

    def remove_points(self, user, points):
        user_profile = self.get(user=user)
        user_profile.points -= int(points)
        user_profile.save()

    def get_points(self, user):
        user_profile = self.get(user=user)
        return user_profile.points

    def get_ranking(self):
        return self.all().order_by('-points')


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.SmallIntegerField(default=0)
    objects = UserProfileManager()

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'

    def __str__(self):
        return self.user.username