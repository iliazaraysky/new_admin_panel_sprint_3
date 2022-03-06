from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.list import BaseListView
from django.views.generic.detail import BaseDetailView

from movies.models import Filmwork, PersonFilmWork, Person


class MoviesApiMixins:
    model = Filmwork
    http_method_names = ['get']  # Список методов, которые реализует обработчик

    def person_to_film(self, role):
        return ArrayAgg(
            'personfilmwork__person__full_name',
            distinct=True, filter=Q(personfilmwork__role=role)
            )

    def person_id(self, role):
        return ArrayAgg(
            'personfilmwork__person__id',
            distinct=True, filter=Q(personfilmwork__role=role)
        )

    def get_queryset(self):
        return Filmwork.objects.values(
            'id',
            'title',
            'description',
            'creation_date',
            'rating',
            'type',
        ).annotate(
            genres=ArrayAgg('genres__name', distinct=True),
            actors=self.person_to_film(role=PersonFilmWork.Role.ACTOR),
            directors=self.person_to_film(role=PersonFilmWork.Role.DIRECTOR),
            writers=self.person_to_film(role=PersonFilmWork.Role.WRITER),
            actors_id=self.person_id(role=PersonFilmWork.Role.ACTOR),
            writers_id=self.person_id(role=PersonFilmWork.Role.WRITER),
            )

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixins, BaseListView):

    def get_context_data(self, *, object_list=None, **kwargs):
        paginate_by = 50
        queryset = self.get_queryset().order_by('id')
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset,
            paginate_by
        )

        context = {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'prev': '',
            'next': '',
            'results': list(paginator.object_list),
        }

        if page.has_previous() == False:
            context['prev'] = None
            context['next'] = page.next_page_number()
        elif page.has_next() == False:
            context['prev'] = page.previous_page_number()
            context['next'] = None
        else:
            context['prev'] = page.previous_page_number()
            context['next'] = page.next_page_number()
        
        return context


class MoviesDetailApi(MoviesApiMixins, BaseDetailView):
    def get_context_data(self, **kwargs):
        object = super(MoviesDetailApi, self).get_object()
        return object
