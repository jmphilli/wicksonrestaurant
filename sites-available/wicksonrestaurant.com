server {
  listen 443 http2 default_server;
  listen [::]:443 http2 default_server;
  root /var/www/wicksonrestaurant.com;
  index index.html;
  server_name wicksonrestaurant.com www.wicksonrestaurant.com;
  location / {
    try_files $uri $uri/ =404;
  }
  ssl on;
  ssl_certificate /etc/letsencrypt/live/wicksonrestaurant.com/fullchain.pem;
  ssl_certificate_key /etc/letsencrypt/live/wicksonrestaurant.com/privkey.pem;

  gzip on;
  gzip_types application/javascript image/* text/css;
  gunzip on;
}

server {
       listen 0.0.0.0:80;
       server_name wicksonrestaurant.com www.wicksonrestaurant.com;
       rewrite ^ https://$host$request_uri? permanent;
}
