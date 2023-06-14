from django.db import models
import os

class NewsItem(models.Model):
    def photo_upload_rename(instance, filename):
        _, ext = os.path.splitext(filename)
        return 'news/{0}/{1}'.format(instance.id, "photo" + ext)

    entity = models.ForeignKey('entity.Entity', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey('affiliate.Affiliate', on_delete=models.PROTECT, related_name='news_items')
    photo = models.ImageField(default="/default_photo.png", upload_to=photo_upload_rename)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at', '-pk')

    def __str__(self):
        return str(self.title)
    
    @property
    def authorstr(self):
        return self.author.name