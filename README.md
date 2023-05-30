# Demo Wagtail app for load testing SQLite

## Installation

Set up Wagtail

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
./manage.py migrate
./manage.py createsuperuser
```

Download 35k film plots and load them into the database:

```bash
python fetch.py https://tomd.org/x/wiki_movie_plots_deduped.csv.gz
gunzip wiki_movie_plots_deduped.csv.gz
./manage.py importfilms
```

Run locally with Gunicorn:

```bash
gunicorn wagtailfilms.wsgi:application
``` 

## Load testing

```bash
# Install wrk
brew install wrk
# Run 5 threads for 5 seconds, read-only
wrk -c5 -d5 -t5 http://127.0.0.1:8000/films/the-test-of-honor/
# Run 5 threads for 5 seconds, read-write
wrk -c5 -d5 -t5 http://127.0.0.1:8000/films/update/
```