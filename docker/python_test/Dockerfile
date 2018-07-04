FROM web

LABEL maintainer="some.email@gmail.com"

# copy the the app directory contents into the container
COPY app /app

# basic flask environment
RUN apk add --no-cache \
	&& pip3 install --upgrade pip \
    && pip3 install -r /app/backend/flask_app/requirements_dev.txt

# expose port
EXPOSE 8181

# run tests
CMD ["python", "-m pytest /app/backend/flask_app/tests"]

