from django.contrib import admin

from .models import Story
from .admin_forms import StoryForm
from .scraper import StoryScraper


@admin.action(description='Fetch Story Data')
def get_story_data(modeladmin, request, queryset):
    story: Story
    for story in queryset:
        story.fetch_data()


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    """
    TODO: Docstring
    """
    form = StoryForm

    list_display = ('title', 'code', 'date', 'get_genres')
    search_fields = ('title', 'code', 'original_title', 'origin')
    list_filter = ('author', 'illustrator', 'characters', 'genre')
    ordering = ('title',)
    actions = [get_story_data, ]
