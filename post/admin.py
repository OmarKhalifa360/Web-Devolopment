from django.contrib import admin
from .models import BlogPost, Comment
# Register your models here.

admin.site.register(BlogPost)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'content', 'post', 'created_date', 'approved_comment')
    list_filter = ('approved_comment', 'created_date')
    search_fields = ('author', 'content')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(approved_comment=True)