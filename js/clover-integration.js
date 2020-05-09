fetch('http://wicksonrestaurant.com:8080/inventory')
  .then(response => response.json())
  .then(data => console.log(JSON.stringify(data)));