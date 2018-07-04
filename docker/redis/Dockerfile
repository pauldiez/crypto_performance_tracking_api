FROM redis:alpine

LABEL maintainer="some.email@gmail.com"

# basic environment
RUN apk upgrade --no-cache \
	&& apk add --no-cache \
	bash

COPY docker/redis/configs/redis.conf /etc/redis/redis.conf

CMD [ "redis-server", "/etc/redis/redis.conf" ]

