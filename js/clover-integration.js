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

const cardNumber = elements.create('CARD_NUMBER', styles);
const cardDate = elements.create('CARD_DATE', styles);
const cardCvv = elements.create('CARD_CVV', styles);
const cardPostalCode = elements.create('CARD_POSTAL_CODE', styles);

cardNumber.mount('#card-number');
cardDate.mount('#card-date');
cardCvv.mount('#card-cvv');
cardPostalCode.mount('#card-postal-code');

const cardResponse = document.getElementById('card-response');
const displayCardNumberError = document.getElementById('card-number-errors');
const displayCardDateError = document.getElementById('card-date-errors');
const displayCardCvvError = document.getElementById('card-cvv-errors');
const displayCardPostalCodeError = document.getElementById('card-postal-code-errors');

  // Handle real-time validation errors from the card element
  cardNumber.addEventListener('change', function(event) {
    console.log(`cardNumber changed ${JSON.stringify(event)}`);
  });

  cardNumber.addEventListener('blur', function(event) {
    console.log(`cardNumber blur ${JSON.stringify(event)}`);
  });

  cardDate.addEventListener('change', function(event) {
    console.log(`cardDate changed ${JSON.stringify(event)}`);
  });

  cardDate.addEventListener('blur', function(event) {
    console.log(`cardDate blur ${JSON.stringify(event)}`);
  });

  cardCvv.addEventListener('change', function(event) {
    console.log(`cardCvv changed ${JSON.stringify(event)}`);
  });

  cardCvv.addEventListener('blur', function(event) {
    console.log(`cardCvv blur ${JSON.stringify(event)}`);
  });

  cardPostalCode.addEventListener('change', function(event) {
    console.log(`cardPostalCode changed ${JSON.stringify(event)}`);
  });

  cardPostalCode.addEventListener('blur', function(event) {
    console.log(`cardPostalCode blur ${JSON.stringify(event)}`);
  });
