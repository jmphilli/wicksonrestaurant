- How to restart nginx - `sudo systemctl restart nginx`
- I used this [readme / guide](https://medium.com/@jgefroh/a-guide-to-using-nginx-for-static-websites-d96a9d034940)
- I configured nginx to host a "staging" site on port 8080. Push new content to the `/var/www/wicksonrestaurant-staging` dir first to confirm changes look good before `cp`ing that dir to `/var/www/wicksonrestaurant.com`

__deploying__
- use `scp-script`
- verify in staging (:8080)
- push to prod `./go-live.sh` on the prod host


- email
  - gmail auth for from + history
  - curl / wget the receipt clover email
  - use that as body
  - add info about pickup time / location (window behind the yadda yadda)

- allow the user to add items to a "cart"
  - tip - need place to add it (cart.html)
    - tip - should be sent over as a % param and let server do it when advancing to customer.html
  - render order details somewhere
  - make page pretty
  - todo allow removal of items (it's probably all js side so whatevs)
  - add to top level menu so people can navigate
  - top of cart - blob of text about how to pickup + timing
  - rename cart.html -> order.html?
  - order details / summary builds on this page too

- on successful charge
  - send email

- customer info on payment / order confirmation
- order confirmation modal
- robots.txt dont let goog scrape the flow

- limit orders per day -
- limit Pickup today v tomorrow by time?
