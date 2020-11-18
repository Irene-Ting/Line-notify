from django.db import models

# Create your models here.

class line_user(models.Model):
    token = models.CharField(max_length=50, verbose_name='access token', default='')
    target_type = models.CharField(max_length=5, verbose_name='target type', default='')
    target = models.CharField(max_length=50, verbose_name='target', default='')
    
    def __str__(self):
        return f"{self.target}"
