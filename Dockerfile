FROM debian:9

RUN apt-get update && apt-get install -y nginx

COPY app /etc/nginx/sites-available/

RUN ln -s /etc/nginx/sites-available/app /etc/nginx/sites-enabled/app

COPY app.html /var/www/html/

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
