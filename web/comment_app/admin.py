from django.contrib import admin
from haystack.admin import SearchModelAdmin

from .models import Comment


class CommentAdmin(SearchModelAdmin):
    list_display = ('order_id', 'author', 'text', 'time_created')
    list_filter = ('author__username', 'time_created',)
    search_fields = ('text',)


admin.site.register(Comment, CommentAdmin)
