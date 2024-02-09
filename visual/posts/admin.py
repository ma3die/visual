from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):
    exclude = ['slug']

admin.site.register(Post, PostAdmin)
