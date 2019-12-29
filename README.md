- How to restart nginx - `sudo systemctl restart nginx`
- I used this [readme / guide](https://medium.com/@jgefroh/a-guide-to-using-nginx-for-static-websites-d96a9d034940)
- I configured nginx to host a "staging" site on port 8080. Push new content to the `/var/www/wicksonrestaurant-staging` dir first to confirm changes look good before `cp`ing that dir to `/var/www/wicksonrestaurant.com`

deploying - 
Do some scp
```bash
scp -r ~/go/src/github.com/jmphilli/wicksonrestaurant/*.html box:/var/www/wicksonrestaurant-staging.com/
scp -r ~/go/src/github.com/jmphilli/wicksonrestaurant/css box:/var/www/wicksonrestaurant-staging.com/
```

Copying from staging to prod:
In the `/var/www/` dir
```bash
cp -Tr wicksonrestaurant-staging.com wicksonrestaurant.com
```
