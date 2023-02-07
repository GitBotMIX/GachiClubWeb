from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from Home.models import Quests, UserProfile


class RouletteItems(models.Model):
    quest = models.ForeignKey(Quests, verbose_name='Задание', on_delete=models.CASCADE, null=True, blank=True)
    is_custom_quest = models.BooleanField(default=False, verbose_name='Сделать кастомный предмет')
    custom_title = models.CharField(db_index=True, max_length=20, verbose_name='Кастомное название', null=True,
                                    blank=True)
    custom_description = models.CharField(db_index=True, max_length=200, verbose_name='Кастомное описание', null=True,
                                          blank=True)
    custom_reward = models.SmallIntegerField(db_index=True, verbose_name='Кастомная награда', null=True, blank=True)
    custom_color = models.CharField(db_index=True, max_length=15, verbose_name='Кастомный цвет', null=True, blank=True)

    class Meta:
        ordering = ('quest__reward',)
        verbose_name = 'Предметы рулетки'
        verbose_name_plural = 'Предметы рулетки'

    def save(self, *args, **kwargs):
        if not self.is_custom_quest and (self.custom_title is not None or self.custom_reward is not None):
            raise ValidationError("custom_quest and custom_reward can only be filled if is_custom_quest is True")
        super().save(*args, **kwargs)

    def __str__(self):
        if self.quest:
            return f'{self.quest.title}'
        else:
            return f'{self.custom_title}'

    @staticmethod
    def length():
        return RouletteItems.objects.all().count()

    def get_title(self):
        if self.quest:
            return f'{self.quest.title}'
        else:
            return f'{self.custom_title}'

    def get_description(self):
        if self.quest:
            return f'{self.quest.description}'
        else:
            return f'{self.custom_description}'

    def get_reward(self):
        if self.quest:
            return f'{self.quest.reward}'
        else:
            return f'{self.custom_reward}'

    def get_color(self):
        if self.quest:
            return f'{self.quest.category.color}'
        else:
            return f'{self.custom_color}'


class RouletteHistory(models.Model):
    COMPLETED_STAGES = (
        (0, 'Выполняется'),
        (1, 'Провалено'),
        (2, 'Выполнено'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    completed_quest = models.ForeignKey(RouletteItems, verbose_name='Задание', on_delete=models.CASCADE)
    is_completed_quest = models.BooleanField(default=True, verbose_name='Квест выполнен')
    completed_at = models.DateTimeField(auto_now_add=True, verbose_name='Выполнено')

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ('completed_at',)
        verbose_name = 'История рулетки'
        verbose_name_plural = 'История рулетки'


class RouletteProfileManager(models.Manager):
    def get_last_user_quest(self, user):
        return RouletteHistory.objects.filter(user=user).order_by('-completed_at')[0]

    def add_spin(self, user):
        roulette_user_profile = self.get(user=user)
        roulette_total_spin = roulette_user_profile.total_spin + 1
        roulette_user_profile.total_spin = roulette_total_spin
        roulette_user_profile.save()
        return roulette_total_spin

    def add_completed_quest(self, user, completed_quest, user_profile=None):
        print(user)
        if user_profile:
            roulette_user_profile = user_profile
        else:
            roulette_user_profile = self.get(user=user)
        roulette_user_profile.total_completed_quest += 1
        roulette_user_profile.quest_in_progress = None
        roulette_user_profile.save()

        last_user_quest_history = self.get_last_user_quest(user)
        last_user_quest_history.is_completed_quest = True
        last_user_quest_history.save()
        UserProfile.objects.add_points(user, str(completed_quest.get_reward()))

    def add_not_completed_quest(self, user, not_completed_quest, user_profile=None):
        if user_profile:
            roulette_user_profile = user_profile
        else:
            roulette_user_profile = self.get(user=user)
        roulette_user_profile.total_not_completed_quest += 1
        roulette_user_profile.quest_in_progress = None
        roulette_user_profile.save()

        UserProfile.objects.remove_points(user, '10')


class RouletteUserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    quest_in_progress = models.ForeignKey(RouletteItems, on_delete=models.CASCADE, verbose_name='Выполняемое задание',
                                          null=True, blank=True)
    total_spin = models.SmallIntegerField(db_index=True, verbose_name='Всего прокручено', default=0)
    total_completed_quest = models.SmallIntegerField(verbose_name='Всего выполненных заданий', default=0)
    total_not_completed_quest = models.SmallIntegerField(verbose_name='Всего выполненных заданий', default=0)
    objects = RouletteProfileManager()

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профиль пользователя'


