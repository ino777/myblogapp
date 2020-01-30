""" Main app(blogs) model """
import datetime
from uuid import uuid4
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import get_user_model
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


User = get_user_model()


# Create your models here.
class Post(models.Model):
    """ Post model """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    text = models.TextField(null=True)
    image = models.ImageField(upload_to=settings.POST_IMAGE_UPLOAD_DIR, verbose_name='post image')
    image_thumbnail = ImageSpecField(
        source='image', processors=[ResizeToFill(640, 360)], format='JPEG', options={'quality': 60})
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True, default=timezone.now)

    def __str__(self):
        return self.title

    def publish(self):
        """ Publish this post now """
        self.published_date = timezone.now()
        self.save()

    def create(self, author):
        """ Create post """
        self.author = author
        self.publish()

    def was_published_recently(self):
        """ Whether the post was published within 1 day """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.published_date <= now
    was_published_recently.admin_order_field = 'published_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    def change_image_name(self, name):
        """ Change the post image name """
        self.image.name = name


class PostEval(models.Model):
    """ Post evaluation (good or bad) """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    good = models.BooleanField(default=False)
    bad = models.BooleanField(default=False)

    created_date = models.DateTimeField(default=timezone.now)


class PostFavorites(models.Model):
    """ A model for bookmarking post """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    favorite = models.BooleanField(default=False)

    created_date = models.DateTimeField(default=timezone.now)


class UserFavorites(models.Model):
    """ A model for bookmarking user """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userfavorite_set')
    target = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_befavorited_set')

    favorite = models.BooleanField(default=False)

    created_date = models.DateTimeField(default=timezone.now)


class PostHit(models.Model):
    """ Post hit model """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    hit = models.BooleanField(default=False)

    created_date = models.DateTimeField(default=timezone.now)


class Comment(models.Model):
    """ Comment model """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    text = models.TextField(max_length=200)

    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(default=timezone.now)
    was_updated = models.BooleanField(default=False)


class CommentReply(models.Model):
    """ A reply for comment model"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    target = models.ForeignKey(Comment, on_delete=models.CASCADE)

    text = models.TextField(max_length=200)

    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(default=timezone.now)
    was_updated = models.BooleanField(default=False)
    
