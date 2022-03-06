from django.contrib import admin
from .models import Genre, Filmwork, GenreFilmwork, PersonFilmWork


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork
    raw_id_fields = ['genre']

class PersonFilmWorkInline(admin.TabularInline):
    model = PersonFilmWork
    raw_id_fields = ['person']

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    list_prefetch_related = ('title',)
    inlines = (GenreFilmworkInline, PersonFilmWorkInline)


@admin.register(PersonFilmWork)
class PersonAdmin(admin.ModelAdmin):
    pass
