from django.contrib import admin

from .models import Gifts, Category, Quests, UserQuests, UserProfile
from roulette.models import RouletteItems, RouletteHistory, RouletteUserProfile

admin.site.register(Gifts)
admin.site.register(Category)
admin.site.register(Quests)
admin.site.register(UserQuests)
admin.site.register(UserProfile)
admin.site.register(RouletteItems)
admin.site.register(RouletteHistory)
admin.site.register(RouletteUserProfile)