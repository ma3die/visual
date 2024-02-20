from django.contrib import admin
from .models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    exclude = ['slug']


admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
