FROM django:python3-onbuild
# RUN useradd z_rank
ENTRYPOINT uwsgi --http 0.0.0.0:8000 --file z_rank/wsgi.py --static-map=/static=static
