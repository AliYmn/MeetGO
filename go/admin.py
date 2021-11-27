from django.contrib import admin

from .models import Category,Events,Profile

class CategoryModel(admin.ModelAdmin):
    list_display = ['title']
    ordering = ['title']
    search_felds = ['title']


class EventsModel(admin.ModelAdmin):
    list_display = ['title',]
    ordering = ['title']
    search_felds = ['title']


admin.site.register(Events,EventsModel)
admin.site.register(Category,CategoryModel)
admin.site.register(Profile)
