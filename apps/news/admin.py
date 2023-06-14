from django.contrib import admin
from .models import NewsItem

class NewsItemAdmin(admin.ModelAdmin):
    list_filter = ("entity",)
    list_display = ("entity", "title", "author")

admin.site.register(NewsItem)