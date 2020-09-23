from django.db import models
from datetime import date
from django.urls import reverse


class Category(models.Model):
    name = models.CharField('Категорія', max_length=32)
    description = models.TextField('Опис')
    url = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'


class Actor(models.Model):
    name = models.CharField('Імя і прізвище', max_length=64)
    age = models.PositiveIntegerField('Вік', default=0)
    description = models.TextField('Опис')
    image = models.ImageField('Фотографія', upload_to='actors/')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Актор або режисер'
        verbose_name_plural = 'Актори і режисери'

    def get_absolute_url(self):
        return reverse('movies:actor_detail', kwargs={"slug": self.name})


class Genre(models.Model):
    name = models.CharField('Назва жанру', max_length=32)
    description = models.TextField('Опис')
    url = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанри'


class Movie(models.Model):
    title = models.CharField('Назва', max_length=128)
    url = models.SlugField(unique=True)
    draft = models.BooleanField('Чорновик?', default=False)
    tagline = models.CharField('Девіз', max_length=128, blank=True)
    description = models.TextField('Опис')
    poster = models.ImageField('Постер', upload_to='movies/')
    year = models.PositiveIntegerField('Рік виходу', default='2020')
    country = models.CharField('Країна', max_length=32)
    directors = models.ManyToManyField(Actor, related_name='film_director', verbose_name='Режисери')
    actors = models.ManyToManyField(Actor, related_name='film_actor', verbose_name='Актори')
    genres = models.ManyToManyField(Genre, verbose_name='Жанри')
    category = models.ForeignKey(Category, verbose_name='Категорія', on_delete=models.SET_NULL, null=True)
    world_premiere = models.DateField('Світова премєра', default=date.today)
    budget = models.PositiveIntegerField('Бюджет', default=0, help_text='Вказувати в USD')
    fees_in_usa = models.PositiveIntegerField('Збори в США', default=0, help_text='Вказувати в USD')
    fees_in_world = models.PositiveIntegerField('Світові збори', default=0, help_text='Вказувати в USD')

    def get_review(self):
        return self.review_set.filter(parent__isnull=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('movies:movie_detail', args=[self.url])

    class Meta:
        verbose_name = 'Фільм'
        verbose_name_plural = 'Фільми'


class MovieShots(models.Model):
    title = models.CharField('Заголовок', max_length=32)
    description = models.TextField('Опис')
    movie = models.ForeignKey(Movie, verbose_name='Фільм', on_delete=models.CASCADE, null=True)
    image = models.ImageField('Кадри', upload_to='movie_shots/')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Кадри з фільму'
        verbose_name_plural = 'Кадри з фільмів'


class RatingStar(models.Model):
    value = models.SmallIntegerField('Значення', default=0)

    def __str__(self):
        return str(self.value)

    class Meta:
        verbose_name = 'Зірка рейтингу'
        verbose_name_plural = 'Зірки рейтингу'
        ordering = ["-value"]


class Rating(models.Model):
    ip = models.CharField(max_length=32)
    star = models.ForeignKey(RatingStar, verbose_name='Зірочка', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, verbose_name='Фільм', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.star} - {self.movie}"

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'


class Review(models.Model):
    email = models.EmailField()
    name = models.CharField('Імя', max_length=32)
    text = models.TextField('Текст', max_length=3000)
    parent = models.ForeignKey('self', verbose_name="Батько", on_delete=models.SET_NULL, blank=True, null=True)
    movie = models.ForeignKey(Movie, verbose_name='', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.movie}"

    class Meta:
        verbose_name = 'Відгук'
        verbose_name_plural = 'Відгуки'
