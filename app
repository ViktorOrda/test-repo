server {
    listen 80;
    listen [::]:80;
    root /var/www/html;
    server_name app.com;

    location / {
      index app.html;
    }

    location /app {
      try_files  $uri $uri.html
      index app.html;
    }

}
