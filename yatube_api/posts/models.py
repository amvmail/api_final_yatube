from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.constraints import UniqueConstraint

User = get_user_model()


class Group(models.Model):
    """Группа."""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField('Описание группы')

    class Meta:
        """Дополнительные параметры Group."""
        verbose_name = 'Группа'
        ordering = ('title',)

    def __str__(self):
        return self.title


class Post(models.Model):
    """Пост."""
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts',
        verbose_name='Автор')
    group = models.ForeignKey(
        Group, on_delete=models.SET_NULL, null=True,
        blank=True, related_name='posts',
        verbose_name='Группа')
    image = models.ImageField(
        upload_to='posts/', null=True, blank=True)

    class Meta:
        """Дополнительные параметры Post."""
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Комментарии."""
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Автор комментария')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Пост')
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        """Дополнительные параметры Comment."""
        ordering = ('-created',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text


class Follow(models.Model):
    """Подписка на посты."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор постов',
        related_name='following'
    )

    class Meta:
        """Дополнительные параметры Follow."""
        constraints = [
            UniqueConstraint(
                fields=['user', 'following'], name='follow_unique'
            ),
        ]

    def __str__(self):
        return f'{self.user} подписан на {self.following}'
