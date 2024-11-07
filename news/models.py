from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from taggit.managers import TaggableManager
import os


class NewsArticle(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', default='default.jpg')
    tags = TaggableManager()
    category = models.CharField(max_length=50, default="general")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        img = Image.open(self.image.path)
        
        target_width, target_height = 800, 500
        aspect_ratio = target_width / target_height
        
        img_ratio = img.width / img.height

        if img_ratio > aspect_ratio:
            new_width = int(aspect_ratio * img.height)
            left = (img.width - new_width) / 2
            right = (img.width + new_width) / 2
            img = img.crop((left, 0, right, img.height))
        elif img_ratio < aspect_ratio:
            new_height = int(img.width / aspect_ratio)
            top = (img.height - new_height) / 2
            bottom = (img.height + new_height) / 2
            img = img.crop((0, top, img.width, bottom))

        img = img.resize((target_width, target_height), Image.LANCZOS)
        
        img.save(self.image.path, quality=75, optimize=True)

    def delete(self, *args, **kwargs):
        if self.image and os.path.isfile(self.image.path) and self.image.name != 'default.jpg':
            os.remove(self.image.path)
        super().delete(*args, **kwargs)

class NewsArticleLike(models.Model):
    article = models.ForeignKey(NewsArticle, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('article', 'user')

    def __str__(self):
        return f'{self.user.username} likes {self.article.title}'

class Comment(models.Model):
    article = models.ForeignKey(NewsArticle, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.article.title}'

