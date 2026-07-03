from django.db import models


class DevTool(models.Model):
    name = models.CharField(max_length=50)
    kind = models.CharField(max_length=50)
    content = models.TextField()

    def __str__(self):
        return self.name


class Idea(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='idea_images/')
    content = models.TextField()
    interest = models.IntegerField(default=0)
    devtool = models.ForeignKey(
        DevTool,
        on_delete=models.CASCADE,
        related_name='ideas'
    )
    is_starred = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class IdeaStar(models.Model):
    idea = models.OneToOneField(
        Idea,
        on_delete=models.CASCADE,
        related_name='star'
    )
    is_starred = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.idea.title} - {self.is_starred}'