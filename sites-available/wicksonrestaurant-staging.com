server {
  listen 8080 default_server;
  listen [::]:8080 default_server;
  root /var/www/wicksonrestaurant-staging.com;
  index index.html;
  server_name wicksonrestaurant-staging.com www.wicksonrestaurant-staging.com;
  location / {
    try_files $uri $uri/ =404;
  }
}