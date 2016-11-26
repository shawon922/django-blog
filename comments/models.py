from django.db import models
from django.conf import settings

from posts.models import Post


class Comment(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL)
    post_id = models.ForeignKey(Post)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user_id.username)
