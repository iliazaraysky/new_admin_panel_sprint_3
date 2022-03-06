import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField('Название', max_length=255)
    description = models.TextField('Описание', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField('Полное имя', max_length=140)

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = "content\".\"person"
        verbose_name = 'Участники фильма'
        verbose_name_plural = 'Участники фильмов'


class Filmwork(UUIDMixin, TimeStampedMixin):
    class Type(models.TextChoices):
        MOVIE = 'movie', _('movie')
        TV_SHOW = 'TV series', _('TV series')

    title = models.CharField('Название фильма', max_length=255)
    genres = models.ManyToManyField(Genre, through='GenreFilmwork')
    description = models.TextField(
        'Описание фильма',
        blank=True,
    )
    creation_date = models.DateField('Дата создания')
    rating = models.FloatField(
        'Рейтинг',
        blank=True,
        validators=[MinValueValidator(0),
                    MaxValueValidator(100)]
    )
    type = models.CharField(
        'Тип',
        max_length=9,
        choices=Type.choices,
    )

    def __str__(self):
        return self.title

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=('film_work_id', 'genre_id'),
                         name='film_work_genre'),
        ]
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        db_table = "content\".\"genre_film_work"


class PersonFilmWork(UUIDMixin):
    class Role(models.TextChoices):
        ACTOR = 'actor', _('actor')
        PRODUCER = 'producer', _('producer')
        DIRECTOR = 'director', _('director')
        WRITER = 'writer', _('writer')

    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    role = models.TextField('role', max_length=15, choices=Role.choices, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.person.full_name

    class Meta:
        verbose_name = 'Участники проекта'
        verbose_name_plural = 'Участники проекта'
        db_table = "content\".\"person_film_work"
