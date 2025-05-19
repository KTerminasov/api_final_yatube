from django.contrib import admin

from .models import Post, Group, Comment, Follow


class PostAdmin(admin.ModelAdmin):
    list_display = ['text', 'pub_date', 'author', 'group']


class GroupAdmin(admin.ModelAdmin):
    list_display = ['title']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['text']


class FollowAdmin(admin.ModelAdmin):
    list_display = ['user', 'following']


admin.site.register(Post, PostAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Follow, FollowAdmin)
