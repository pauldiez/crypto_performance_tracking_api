FROM python:alpine3.6

LABEL maintainer="some.email@gmail.com"

RUN set -x ; \
  addgroup -g 82 -S www-data ; \
  adduser -u 82 -D -S -G www-data www-data && exit 0 ; exit 1

# copy the the app directory contents into the container
COPY app/backend/flask_app/requirements.txt /requirements.txt

# basic flask environment
RUN apk --upgrade \
    --no-cache add linux-headers \
	build-base \
	postgresql-dev \
	gcc \
	libffi-dev \
	python3-dev \
	musl-dev \
	bash \
	openssl \
	coreutils \
	easy-rsa

ENV BUILD_DEPS="gettext"  \
    RUNTIME_DEPS="libintl"

RUN set -x && \
    apk add --update $RUNTIME_DEPS && \
    apk add --virtual build_deps $BUILD_DEPS &&  \
    apk add --no-cache --virtual .gettext gettext && \
    cp /usr/bin/envsubst /usr/local/bin/envsubst && \
    apk del build_deps && \
    apk del .gettext

RUN pip3 install --upgrade pip setuptools \
    && pip3 install -r /requirements.txt

# expose web server port
# only http, for ssl use reverse proxy
EXPOSE 8080

# run uwsgi locally
#CMD ["uwsgi", "/etc/uwsgi/uwsgi-local.ini"]

# run uwsgi via nginx
#CMD ["uwsgi", "/etc/uwsgi/uwsgi.ini"]

# run via python (without uwsgi server)
CMD ["python"]

# exectute start up script
#ENTRYPOINT ["/entrypoint.sh"]


### DOCS ###

# Running the uwsgi server
#https://uwsgi-docs.readthedocs.io/en/latest/WSGIquickstart.html

#BUILD
# docker build -t python_uwsgi_img .

#RUN EXAMPLES
# docker run --name=python_uwsgi_ctnr --hostname=python --rm -it -p 80:80 --mount type=bind,source=$("pwd")/app,target=/app python_uwsgi_img bash -c "uwsgi --http :80 --wsgi-file application.py --py-autoreload=2"
#CMD ["uwsgi", "--http :80", "--wsgi-file application.py"]

# Flask exports its WSGI function (the one we called “application” at the beginning of this quickstart) as “app”, so we need to instruct uWSGI to use it.
# docker run --name=python_uwsgi_cntr --hostname=python --rm -it -p 80:80 --mount type=bind,source=$("pwd")/app,target=/app python_uwsgi_img bash -c "uwsgi --http :80 --wsgi-file app_old.py --callable app --py-autoreload=2"
#CMD ["uwsgi", "--http :80", "--wsgi-file app_old.py", "--callable app"]
