from django.contrib import admin
from .models import Idea, DevTool, IdeaStar


@admin.register(DevTool)
class DevToolAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'kind')
    search_fields = ('name', 'kind')


@admin.register(Idea)
class IdeaAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'devtool', 'interest', 'is_starred', 'created_at')
    list_filter = ('devtool', 'is_starred')
    search_fields = ('title', 'content')

@admin.register(IdeaStar)
class IdeaStarAdmin(admin.ModelAdmin):
    list_display = ('id', 'idea', 'is_starred')