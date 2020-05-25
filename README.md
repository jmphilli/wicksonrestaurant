- How to restart nginx - `sudo systemctl restart nginx`
- I used this [readme / guide](https://medium.com/@jgefroh/a-guide-to-using-nginx-for-static-websites-d96a9d034940)
- I configured nginx to host a "staging" site on port 8080. Push new content to the `/var/www/wicksonrestaurant-staging` dir first to confirm changes look good before `cp`ing that dir to `/var/www/wicksonrestaurant.com`

__deploying__
- use `scp-script`
- verify in staging (:8080)
- push to prod `./go-live.sh` on the prod host


__plan for pickup + dine in__

I'm using this as my design doc...
I think what i want to do is

- allow the user to add items to a "cart"
  - todo allow removal of items (it's probably all js side so whatevs)
- allow the user to "checkout"
  - push them over to a stripe charge given the sum of line items + taxes
- on success
  - update the order in the clover stack to have the associated charge
  - render some sorta order number / id to the user so they know which one they were
- on fail
  - just drop all state and let them go back
- tip + taxes
- render total on page
- metadata on clover order
  - stripe token for successful charge
  - schedule / dietary restrictions saved in order as well
  - customer name for pickup
- make page pretty
- add to top level menu so people can navigate
- possibly open orders@wicksonrestaurant.com
- same with support@wicksonrestaurant.com
- blurb about restaurant stataus somewhere "starting june 1 we are accepting seating etc etc"
- send email when order ready
-  Order Total: $0.00 set the order total for clover
