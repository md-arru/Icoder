from django.contrib import admin
from blog.models import Post, BlogComment
# Register your models here.

admin.site.site_header = "BlogFriends Admin"
admin.site.site_title = "BlogFriends Admin Panel"
admin.site.index_title = "Welcome to  BlogFriends Admin"


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    class Media:
        js = ('tinyInject.js')


admin.site.register(BlogComment)
