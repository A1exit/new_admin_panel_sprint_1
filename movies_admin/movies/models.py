import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin, models.Model):
    name = models.CharField(
        _('name'),
        max_length=255,
    )
    description = models.TextField(
        _('description'),
        blank=True,
        null=True
    )

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Filmwork(UUIDMixin, TimeStampedMixin, models.Model):
    title = models.CharField(
        _('title'),
        max_length=255,
    )
    description = models.TextField(
        _('description'),
        blank=True,
        null=True
    )
    creation_date = models.DateTimeField(
        _('creation date'),
        auto_now=True,
        blank=True,
        null=True
    )
    rating = models.FloatField(
        _('rating'),
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=True
    )

    class Type(models.TextChoices):
        movie = 'movie'
        tv_show = 'tv_show'

    type = models.CharField(
        _('type'),
        max_length=10,
        choices=Type.choices,
    )
    genres = models.ManyToManyField(
        Genre, through='GenreFilmwork'
    )
    file_path = models.FileField(
        _('file'),
        blank=True,
        null=True,
        upload_to='movies/'
    )

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = 'Кинопроизведение'
        verbose_name_plural = 'Кинопроизведения'

    def __str__(self):
        return self.title


class GenreFilmwork(UUIDMixin, models.Model):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    created = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        null=True
    )

    class Meta:
        db_table = "content\".\"genre_film_work"


class Person(UUIDMixin, TimeStampedMixin, models.Model):
    full_name = models.CharField(
        _('full name'),
        max_length=100,
    )
    filmwork = models.ManyToManyField(Filmwork, through='PersonFilmwork')

    class Meta:
        db_table = "content\".\"person"
        verbose_name = 'Человек'
        verbose_name_plural = 'Люди'

    def __str__(self):
        return self.full_name


class PersonFilmwork(UUIDMixin, models.Model):
    film_work = models.ForeignKey(
        'Filmwork', on_delete=models.CASCADE,
    )
    person = models.ForeignKey(
        'Person', on_delete=models.CASCADE,
    )

    class Role(models.TextChoices):
        actor = 'actor'
        director = 'director'
        screenwriter = 'screenwriter'

    role = models.CharField(
        _('role'),
        max_length=12,
        choices=Role.choices,
        blank=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = "content\".\"person_film_work"
        UniqueConstraint(
            fields=['film_work_id', 'person_id', 'role'],
            name='unique_film_work_person_role'
        )
