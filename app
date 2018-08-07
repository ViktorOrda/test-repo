server {
    listen 80;
    listen [::]:80;
    root /var/www/html;
    server_name app.com;

    location / {
      index index.html index.htm index.nginx-debian.html app.html;
    }

    location /app {
      try_files  $uri $uri.html
      index app.html;
    }

}
