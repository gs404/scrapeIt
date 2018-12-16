from django.db import models

# Create your models here.

class Tag(models.Model):
    tag = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return self.tag

class Article(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True, null=True)
    author = models.CharField(max_length=25)
    subtitle = models.CharField(max_length=150, blank=True, null=True)
    cover = models.CharField(max_length=200, blank=True, null=True)
    date = models.CharField(max_length=20, blank=True, null=True)
    readingTime = models.CharField(max_length=10, blank=True, null=True)
    claps = models.CharField(max_length=5, blank=True, null=True)
    link = models.CharField(max_length=200, blank=True, null=True)
    content = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.tag).capitalize() + ' - ' + self.title + ' - ' + self.author

class Response(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    by = models.CharField(max_length=25)
    content = models.TextField()

    def __str__(self):
        return str(self.article).capitalize() + ' - ' + self.by
