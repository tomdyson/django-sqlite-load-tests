from django.db import models
from django.http import HttpResponse
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, path


class FilmIndexPage(RoutablePageMixin, Page):
    def get_context(self, request):
        context = super().get_context(request)
        # list every year that has at least one film
        context["film_years"] = (
            FilmPage.objects.live().order_by("-release_year").values_list(
                "release_year", flat=True
            ).distinct()
        )
        return context
    
    @path('update/')
    def update_random_page(self, request):
        """
        Take a random Film page and update it with the plot of 'Elf'
        """
        elf_plot = FilmPage.objects.get(title='Elf').plot
        random_page = FilmPage.objects.live().order_by('?').first()
        random_page.plot = elf_plot
        random_page.save_revision().publish()
        return HttpResponse(f'Updated {random_page.title} with the plot of Elf')


class FilmPage(Page):
    parent_page_types = ["films.FilmIndexPage"]

    release_year = models.IntegerField("Release year")
    director = models.CharField(max_length=250, blank=True)
    wiki_page = models.URLField()
    plot = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("release_year"),
        FieldPanel("director"),
        FieldPanel("wiki_page"),
        FieldPanel("plot", classname="full"),
    ]

    search_auto_update = False

    def get_context(self, request):
        context = super().get_context(request)
        # get up to five films from the same year
        context["related_films"] = (
            FilmPage.objects.live()
            .filter(release_year=self.release_year)
            .exclude(id=self.id)[:5]
        )
        return context