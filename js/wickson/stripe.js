var publishableIdentifier = 'pk_test_AomxgyKY6zMiPVwT7JYyXyZR00N8k0Cqcb';
var stripe = Stripe(publishableIdentifier);

var elements = stripe.elements();
var cardElement = elements.create('card');
cardElement.mount('#card-element');

var form = document.getElementById('payment-form');
var resultContainer = document.getElementById('payment-result');
cardElement.on('change', function(event) {
  if (event.error) {
    resultContainer.textContent = event.error.message;
  } else {
    resultContainer.textContent = '';
  }
});

form.addEventListener('submit', function(event) {
  event.preventDefault();
  resultContainer.textContent = "";
  stripe.createPaymentMethod({
    type: 'card',
    card: cardElement,
  }).then(handlePaymentMethodResult);
});

function handlePaymentMethodResult(result) {
  if (result.error) {
    // An error happened when collecting card details, show it in the payment form
    resultContainer.textContent = result.error.message;
  } else {
    // Otherwise send paymentMethod.id to your server (see Step 3)
    fetch('/charge', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(
          {
              payment_method_id: result.paymentMethod.id,
              order_id: getOrderId()
          }
          )
    }).then(function(result) {
      return result.json();
    }).then(handleServerResponse);
  }
}

// Redirect to confirmation page
function handleServerResponse(responseJson) {
  if (responseJson.error) {
    // An error happened when charging the card, show it in the payment form
    resultContainer.textContent = responseJson.error;
  } else {
      var orderId = responseJson['order_id'];
      window.location.href = siteUrl + '/order_confirmation.html?order_id=' + orderId;
  }
}
