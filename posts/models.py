from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    """
    Таблица публикаций сообществ.

    Ключевые аргументы:
    title -- название группы
    slug -- формирует URL группы (уникальные значения)
    description -- описание группы
    """
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    class Meta:
        ordering = ("title", )

    def __str__(self):
        return self.title


class Post(models.Model):
    """
    Таблица публикаций.

    Ключевые агрументы:
    text -- текст публикации
    pub_date -- дата публикации(по умолчанию актуальная дата)
    author -- id автора публикации, связано с таблицей User
    group -- id группы, связано с таблицей Group
    """
    text = models.TextField()
    pub_date = models.DateTimeField("date published", auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="posts")
    group = models.ForeignKey(Group, models.SET_NULL, blank=True, null=True,
                              related_name="posts")
    image = models.ImageField(upload_to='posts/', blank=True, null=True)

    class Meta:
        ordering = ("-pub_date", )

    def __str__(self):
        return self.text


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="comments")
    text = models.TextField()
    created = models.DateTimeField("date published", auto_now_add=True)

    class Meta:
        ordering = ("created", )


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="follower")
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="following")

    class Meta:
        unique_together = ("user", "author",)
