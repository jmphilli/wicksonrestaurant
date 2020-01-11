- How to restart nginx - `sudo systemctl restart nginx`
- I used this [readme / guide](https://medium.com/@jgefroh/a-guide-to-using-nginx-for-static-websites-d96a9d034940)
- I configured nginx to host a "staging" site on port 8080. Push new content to the `/var/www/wicksonrestaurant-staging` dir first to confirm changes look good before `cp`ing that dir to `/var/www/wicksonrestaurant.com`

__deploying__ 
- use `scp-script`
- verify in staging (:8080)
- push to prod `./go-live.sh` on the prod host
