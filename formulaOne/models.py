from django.db import models

# Create your models here.
from django.db import models
  
    
class Article(models.Model):
    
    id = models.CharField(max_length=70, blank=False, default='', primary_key=True)
    title = models.CharField(max_length=70, blank=False, default='')
    content = models.TextField(max_length=200, default='')
    created_at = models.DateTimeField(auto_now_add=True)   

def __str__(self):
    return self.title   

