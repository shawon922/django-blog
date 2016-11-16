from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save

from django.utils.text import slugify


def upload_location(instance, filename):
    # return "%s/%s" % (instance.id, filename)
    PostModel = instance.__class__
    new_id = Post.objects.order_by('id').last().id + 1
    
    return "%s/%s" % (new_id, filename)


class Post(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to=upload_location,
                              null=True,
                              blank=True,
                              height_field='height_field',
                              width_field='width_field')
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField()
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts:detail', kwargs={'id': self.id})

    class Meta:
        ordering = ['-timestamp', '-updated']


def create_slug(instance, new_slug=None):
    temp_title = ''
    if len(instance.title) > 40:
        temp_title = instance.title[:40]
    else:
        temp_title = instance.title

    slug = slugify(temp_title)

    if new_slug is not None:
        slug = new_slug

    qs = Post.objects.filter(slug=slug).order_by('-id')

    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, sender=Post)
