const clover = new Clover();
const elements = clover.elements();

const form = document.getElementById('payment-form');
  form.addEventListener('submit', function(event) {
    event.preventDefault();

    clover.createToken()
      .then(function(result) {
        if (result.errors) {
          Object.values(result.errors).forEach(function (value) {
            displayError.textContent = value;
          });
        } else {
          cloverTokenHandler(result.token);
        }
      });
  });