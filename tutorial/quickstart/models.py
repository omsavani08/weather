from django.db import models

# Create your models here.
class Detail(models.Model):
    no = models.IntegerField(primary_key=True)
    city = models.CharField(max_length = 30, null = True, blank = True)
    temperature = models.CharField(max_length = 5, null = True, blank = True)
    
    def __str__(self):
        return self.city
    
