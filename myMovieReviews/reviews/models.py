from django.db import models

class Review(models.Model):
    title = models.CharField(max_length=100)
    director = models.CharField(max_length=100)
    actor = models.CharField(max_length=100)
    genre = models.CharField(max_length=50)
    rating = models.FloatField()
    running_time = models.IntegerField()
    content = models.TextField()
    release_year = models.IntegerField()

    def __str__(self):
        return self.title