from django.contrib import admin

from .models import Gifts, Category, Quests, UserQuests, UserProfile

admin.site.register(Gifts)
admin.site.register(Category)
admin.site.register(Quests)
admin.site.register(UserQuests)
admin.site.register(UserProfile)