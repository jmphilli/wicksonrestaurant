- How to restart nginx - `sudo systemctl restart nginx`
- I used this [readme / guide](https://medium.com/@jgefroh/a-guide-to-using-nginx-for-static-websites-d96a9d034940)
- I configured nginx to host a "staging" site on port 8080. Push new content to the `/var/www/wicksonrestaurant-staging` dir first to confirm changes look good before `cp`ing that dir to `/var/www/wicksonrestaurant.com`

__deploying__
- use `scp-script`
- verify in staging (:8080)
- push to prod `./go-live.sh` on the prod host


- schedule
  - table availability - reserving
  - day before
    - break out schedule for when they want to pickup - start with dropdown of hours
    - add dine in option

- tip - need place to add it (cart.html)

- email
  - gmail auth for from + history
  - curl / wget the receipt clover email
  - use that as body

- allow the user to add items to a "cart"
  - make page pretty
  - todo allow removal of items (it's probably all js side so whatevs)
  - add to top level menu so people can navigate

- allow the user to "checkout"
- on success
  - send email
- on fail
  - just drop all state and let them go back

- dine in only collect email
