from django.db import models
from django.db.models import Count

from account.models import Author


class Abstract(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class News(Abstract):
    text = models.TextField()

    def __str__(self):
        return f'News {self.id} by {self.author.user.username}'

    def get_status(self):
        statuses = NewsStatus.objects.filter(news=self)\
        .values('status__name').annotate(count=Count('status'))
        result = {}
        for i in statuses:
            result[i['status__name']] = i['count']

        return result


class Comment(Abstract):
    news = models.ForeignKey(News, on_delete=models.CASCADE)

    def __str__(self):
        return f'Comment {self.id} by {self.author.user.username} to {self.news.id}'

    def get_status(self):
        statuses = CommentStatus.objects.filter(comment=self) \
            .values('status__name').annotate(count=Count('status'))
        result = {}
        for i in statuses:
            result[i['status__name']] = i['count']

        return result


class Status(models.Model):
    slug = models.SlugField()
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class NewsStatus(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.SET_DEFAULT, default=1)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['news', 'author']

    def __str__(self):
        return f'{self.news.id} - {self.author} - {self.status}'


class CommentStatus(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.SET_DEFAULT, default=1)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['comment', 'author']

    def __str__(self):
        return f'{self.comment.id} - {self.author} - {self.type}'

