import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _


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
    name = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(
        'Имя', max_length=255,
        unique=True, null=False, blank=False
    )

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = "content\".\"person"
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'


class Filmwork(UUIDMixin, TimeStampedMixin):
    class Type(models.TextChoices):
        M = 'movie', 'movie'
        T = 'tv_show', 'tv_show'

    title = models.CharField(
        'Название', max_length=255,
        unique=True, null=False, blank=False
    )
    description = models.TextField(_('description'), null=True, blank=True)
    creation_date = models.DateField(_('creation date'))
    rating = models.FloatField(
        _('rating'), blank=True, null=True,
        validators=[
            MinValueValidator(0), MaxValueValidator(100)
        ])
    type = models.CharField(
        _('type'), max_length=7,
        choices=Type.choices, default=Type.M)
    genres = models.ManyToManyField(Genre, through='GenreFilmwork')

    def __str__(self):
        return self.title

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey(Filmwork, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"


class PersonFilmwork(UUIDMixin):
    film_work = models.ForeignKey(Filmwork, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    role = models.TextField('role')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"
