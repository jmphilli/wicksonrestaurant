function setCustomerDetails(firstName, lastName, email, phone) {
    var node = document.querySelector('#customer-details');
    node.innerHTML = firstName + lastName + email + phone;
}

function getCustomer() {
    var orderId = getOrderId();
    return fetch(siteUrl + '/customer', {
        headers: { "Content-Type": "application/json; charset=utf-8" },
        method: 'GET',
        body: JSON.stringify({
            order_id: orderId,
        })
    })
        .then(
            response => response.json()
        )
        .then(
            customer => {
                var firstName = customer.first_name;
                var lastName = customer.last_name;
                var email = customer.email;
                var phone = 'todo';
                setCustomerDetails(firstName, lastName, email, phone);
            }
            );
}

getCustomer();
