FROM nginx:mainline-alpine

LABEL maintainer="some.email@gmail.com"

# expose web server port
# only http, for ssl use reverse proxy
EXPOSE 80

# basic environment
RUN apk upgrade --no-cache \
	&& apk add --no-cache \
	bash

# copy config files into filesystem
#COPY docker/nginx/configs/nginx.conf /etc/nginx/nginx.conf
#COPY docker/nginx/configs/conf.d/flaskapp.com.conf /etc/nginx/conf.d/

######################################################################
#http://www.patricksoftwareblog.com/how-to-configure-nginx-for-a-flask-web-application/
#http://www.ameyalokare.com/docker/2017/09/20/nginx-flask-postgres-docker-compose.html

#BUILD
# docker build -t nginx_img .

#RUN EXMAPLE
# always remove after exit
# docker run --name nginx_ctnr --hostname web --rm -it -p 80:80 nginx

# always restart after an exit
# docker run --name nginx_ctnr --hostname web  --restart=always -it -p 80:80 nginx

### To get a copy of the nginx config files run the following commands
# docker run --name tmp-nginx-container -d nginx:apline
# docker cp tmp-nginx-container:/etc/nginx/nginx.conf.old /host/path/nginx.conf.old
# docker cp tmp-nginx-container:/etc/nginx/conf.d/ /host/path/conf.d_old
# docker rm -f tmp-nginx-container