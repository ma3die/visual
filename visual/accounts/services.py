from .models import Account
from posts.models import Post


def my_post(user):
    return Post.objects.filter(author_id=user.id)