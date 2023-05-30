import csv
from tqdm import tqdm
from django.core.management.base import BaseCommand
from wagtail.models import Page
from films.models import FilmIndexPage, FilmPage


class Command(BaseCommand):
    help = "Imports 35k film plots from Wikipedia"

    def handle(self, *args, **options):
        # delete existing film index pages and film pages
        FilmPage.objects.all().delete()
        FilmIndexPage.objects.all().delete()
        # create a film index page
        home = Page.objects.get(id=3)
        films_index_page = FilmIndexPage(title="Films")
        home.add_child(instance=films_index_page)
        films_index_page.save_revision().publish()
        # import film pages
        # file_path = "wiki-plots-1000.csv"
        file_path = "wiki_movie_plots_deduped.csv"
        num_lines = sum(1 for _ in open(file_path))
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in tqdm(reader, total=num_lines):
                film_page = FilmPage(
                    title=row["Title"],
                    release_year=row["Release Year"],
                    director=row["Director"],
                    wiki_page=row["Wiki Page"],
                    plot=row["Plot"],
                )
                films_index_page.add_child(instance=film_page)
                film_page.save_revision().publish()
                # print("published film page " + row["Title"])