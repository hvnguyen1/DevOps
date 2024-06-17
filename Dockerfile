# Pull base image
FROM debian:latest

# Dockerfile Maintainer
MAINTAINER Benjamin Le

# Install nginx and adjust nginx config to stay in foreground
RUN apt-get update && apt-get install --no-install-recommends -y nginx

COPY static-site/index.html /usr/share/nginx/html/
COPY static-site/index.css /usr/share/nginx/html/
COPY static-site/nginx.conf /etc/nginx/nginx.conf

EXPOSE 9080
CMD ["nginx", "-g", "daemon off;"]
