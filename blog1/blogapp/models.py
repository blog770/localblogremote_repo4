from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.urlresolvers import reverse
from taggit.managers import TaggableManager
# Create your models here.
class CustomManager(models.Manager):
    def get_queryset(self):
         return super().get_queryset().filter(status='published')

class Post(models.Model):
    status_choicess=(('draft','DRAFT'),('published','PUBLISHED'))
    title=models.CharField(max_length=264)
    slug=models.SlugField(max_length=264,unique_for_date='publish')
    author=models.ForeignKey(User,related_name='blog_posts')
    body=models.TextField()
    publish=models.DateField(default=timezone.now)
    created=models.DateField(auto_now_add=True)
    updated=models.DateField(auto_now=True)
    status=models.CharField(max_length=264,choices=status_choicess,default='draft')
    objects=CustomManager()
    tags=TaggableManager()
    
    class Meta:
        ordering=('-publish',)
    def get_absolute_url(self):
        return reverse('post_detail',args=[self.publish.year,self.publish.strftime('%m'),self.publish.strftime('%d'),self.slug])
#model related to comments section
class Comment(models.Model):
    post=models.ForeignKey(Post,related_name='comments')
    name=models.CharField(max_length=30)
    email=models.EmailField()
    body=models.TextField()
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    active=models.BooleanField(default=True)
    class Meta:
        ordering=('created',)
    def __str__(self):
        return 'commented by {} on {}'.format(self.name,self.post)
