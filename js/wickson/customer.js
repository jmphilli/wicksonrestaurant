function setCustomerDetails(firstName, lastName, email, phone) {
    var firstNameNode = document.querySelector('#customer-first');
    firstNameNode.innerHTML = firstName;
    var lastNameNode = document.querySelector('#customer-last');
    lastNameNode.innerHTML = lastName;
    var emailNode = document.querySelector('#customer-email');
    emailNode.innerHTML = email;
    var phoneNode = document.querySelector('#customer-phone');
    phoneNode.innerHTML = phone;
}

function getCustomer() {
    var orderId = getOrderId();
    return fetch(siteUrl + '/customer?order_id=' + orderId, {
        headers: { "Content-Type": "application/json; charset=utf-8" },
        method: 'GET',
    })
        .then(
            response => response.json()
        )
        .then(
            customer => {
                var firstName = customer.first_name;
                var lastName = customer.last_name;
                var email = customer.email;
                var phone = customer.phone;
                setCustomerDetails(firstName, lastName, email, phone);
            }
            );
}

getCustomer();
