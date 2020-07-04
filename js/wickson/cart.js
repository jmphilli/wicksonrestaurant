// make a request to get every item and return the items
var siteUrl = 'http://wicksonrestaurant.com:8080';  // staging
// var siteUrl = 'https://wicksonrestaurant.com';  // prod

function currencyString(rawAmount) {
    return (rawAmount / 100).toFixed(2)
}
function parseInventoryItem(item) {
    return {
        id: item.id,
        name: item.name,
        price: currencyString(item.price),
        category: item.category,
        // probably add image if they've got it
    };
}

function parseInventory(inventory) {
    var parsedItems = [];
    for (var inventoryItem of inventory) {
        parsedItems.push(parseInventoryItem(inventoryItem))
    }
    return parsedItems;
}

function getInventory() {
    return fetch(siteUrl + '/inventory')
        .then(response => response.json())
        .then(inventory => parseInventory(inventory))
}

function getOrderDetails() {
    var order_id = getOrderId();
    return fetch(siteUrl + '/order-details?order_id=' + order_id, {
        headers: { "Content-Type": "application/json; charset=utf-8" },
        method: 'GET'
    })
        .then(response => response.json())
        .then(details => parseDetails(details))
}

function createInventoryHtml(inventoryItem) {
    return `<div class="m-0 col-lg-6 col-sm-6">${inventoryItem.name} -- \$ ${inventoryItem.price}
<button onclick="addToCart('${inventoryItem.id}')">+</button></div>
<button onclick="removeFromCart('${inventoryItem.id}')">-</button></div>`;
}

function buildHtmlInventory(inventory) {
    var snackString = '';
    var entreeString = '';
    var drinkString = '';
    inventory.forEach(function (inventoryItem) {
        if (inventoryItem.category != null && inventoryItem.category !== undefined) {
            if (inventoryItem.category.toLowerCase() == 'extras') {
                snackString += createInventoryHtml(inventoryItem);
            } else if (inventoryItem.category.toLowerCase() == 'quesadillas') {
                entreeString += createInventoryHtml(inventoryItem);
            } else if (inventoryItem.category.toLowerCase() == 'soup') {
                drinkString += createInventoryHtml(inventoryItem);
            }
        }
    });
    return {
        snacks: snackString,
        drinks: drinkString,
        entrees: entreeString
    };
}

function renderOrderItem(orderItem) {
    var priceString = '$' + currencyString(orderItem['price']);
    return `<div class="m-0 col-lg-6 col-sm-6">${orderItem['name']}</div><div class="m-0 col-lg-6 col-sm-6">${priceString}</div>`;
}

function buildHtmlOrderDetails(orderDetails) {
    var itemsString = '';
    var priceString = `
<h2>Tip</h2>
<div class="m-0 col-lg-6 col-sm-6">${orderDetails['tip']}</div>
<h2>Tax</h2>
<div class="m-0 col-lg-6 col-sm-6">${orderDetails['tax']}</div>
<h2>Service Charge</h2>
<div class="m-0 col-lg-6 col-sm-6">${orderDetails['serviceCharge']}</div>
<h2>Total</h2>
<div class="m-0 col-lg-6 col-sm-6">${orderDetails['totalCost']}</div>
`;
    orderDetails.lineItems.forEach(
        function (orderDetail) {
            if (orderDetail['name'] !== 'tip') {
                itemsString += renderOrderItem(orderDetail);
            }
        }
    );

    return {
        itemBreakdown: itemsString,
        priceBreakdown: priceString,
    }
}

function parseDetails(orderDetails) {
    /*
    {'line_items': [
    {"id": "1E4YJX681Q4N4", "item_id": "M7BVBV780YZN0", "name": "Bowl of Soup", "price": 450}
    'total_cost': 961, 'tax': 3, 'tip': 3}
     */
    var totalCost = currencyString(orderDetails['total_cost']);
    var tax = currencyString(orderDetails['tax']);
    var tip = currencyString(orderDetails['tip']);
    var serviceCharge = currencyString(orderDetails['service_charge']);
    var lineItems = orderDetails['line_items']; // probably mash together total quantity

    return {
        lineItems: lineItems,
        serviceCharge: '$' + serviceCharge,
        tax: '$' + tax,
        tip: '$' + tip,
        totalCost: '$' + totalCost
    }
}

function _render() {
    return getInventory().then(inventory => buildHtmlInventory(inventory));
}

function _render_order_details() {
    return getOrderDetails().then(orderDetails => buildHtmlOrderDetails(orderDetails));
}

function renderInventory() {
    var snackNode = document.querySelector('#snacks');
    if (snackNode == null || snackNode === undefined) {
        return
    }
    var entreeNode = document.querySelector('#entrees');
    var drinksNode = document.querySelector('#drinks');
    _render().then(strings => {
        snackNode.innerHTML = strings.snacks;
        entreeNode.innerHTML = strings.entrees;
        drinksNode.innerHTML = strings.drinks;
    });
}

function renderOrderDetails() {
    var orderDetailsNode = document.querySelector('#order-details');
    if (orderDetailsNode == null || orderDetailsNode === undefined) {
        return // different page rendering
    }
    var itemBreakdownNode = document.querySelector('#item-breakdown');
    var priceBreakdownNode = document.querySelector('#price-breakdown');
    _render_order_details().then(strings => {
        itemBreakdownNode.innerHTML = strings.itemBreakdown;
        priceBreakdownNode.innerHTML = strings.priceBreakdown;
    });
}

function getOrderId() {
    var node = document.querySelector('#order_id');
    var order_id = node.innerHTML;
    if (order_id != null && order_id !== undefined && order_id !== "") {
        return order_id;
    }
    var urlParams = new URLSearchParams(window.location.search);
    order_id = urlParams.get('order_id');
    if (order_id != null && order_id !== undefined) {
        setOrderId(order_id); // so it's on the page now
        return order_id;
    }
}

function setOrderId(orderId) {
    var node = document.querySelector('#order_id');
    node.innerHTML = orderId;
    var formOrderId = document.querySelector('#order-id-form');
    if (formOrderId) {
        formOrderId.value = orderId;
    }
}

function _calculateTotal(order_id) {
    return fetch(siteUrl + '/calculate-order-total', {
        headers: { "Content-Type": "application/json; charset=utf-8" },
        method: 'POST',
        body: JSON.stringify({
            order_id: order_id,
        })
    }).then(response => response.json());
}

function calculateTotal(order_id) {
    _calculateTotal(order_id).then(total => {
        var totalNode = document.querySelector('#total');
        totalNode.innerHTML = "$" + currencyString(total.order_total);
    })
}

function addToCart(inventoryId) {
    var orderId = getOrderId();
    return fetch(siteUrl + '/add-line-item', {
        headers: { "Content-Type": "application/json; charset=utf-8" },
        method: 'POST',
        body: JSON.stringify({
            inventory_item_id: inventoryId,
            order_id: orderId,
        })
    }).then(response => response.json())
        .then(order_body => {
            //todo - if we want state, per browser, between tabs, i can probably use local storage.
            order_id = order_body.order_id;
            setOrderId(order_id);
            calculateTotal(order_id);
    });
}

function removeFromCart(inventoryId) {
    var orderId = getOrderId();
    return fetch(siteUrl + '/remove-line-item', {
        headers: { "Content-Type": "application/json; charset=utf-8" },
        method: 'POST',
        body: JSON.stringify({
            inventory_item_id: inventoryId,
            order_id: orderId,
        })
    }).then(response => response.json())
        .then(order_body => {
            order_id = order_body.order_id;
            setOrderId(order_id);
            calculateTotal(order_id);
    });
}

function addTip(pct, isPercentage) {
    var orderId = getOrderId();
    var tip_amount = 0;
    if (!isPercentage) {
        var customAmount = document.querySelector('#custom-tip');
        tip_amount = parseInt(parseFloat(customAmount.value, 0) * 100);
    }
    return _calculateTotal(orderId).then(_ => {
        // TODO user feedback that it worked
        fetch(siteUrl + '/add-tip', {
            headers: {"Content-Type": "application/json; charset=utf-8"},
            method: 'POST',
            body: JSON.stringify({
                order_id: orderId,
                tip_amount: tip_amount,
                percentage: pct,
            })
        })
            .then(_ => calculateTotal(orderId))
    });
}

function addCustomerToOrder() {
    var orderId = getOrderId();
    var firstName = document.querySelector('#first_name').value;
    var lastName = document.querySelector('#last_name').value;
    var email = document.querySelector('#customer_email').value;
    var phone = document.querySelector('#phone_number').value;
    var note = document.querySelector('#note').value;
    if (!firstName || !lastName){
        alert('name not set');
        return;
    }
    if (!email) {
        alert('email required');
        return;
    }
    if (!phone) {
        alert('phone required');
        return;
    }
    return fetch(siteUrl + '/add-customer', {
        headers: { "Content-Type": "application/json; charset=utf-8" },
        method: 'POST',
        body: JSON.stringify({
            order_id: orderId,
            first_name: firstName,
            last_name: lastName,
            email: email,
            phone: phone,
            note: note
        })
    })
        .then(
            response => response.json()
        )
        .then(
            order_body => {
                order_id = order_body.order_id;
                setOrderId(order_id);
                window.location.href = siteUrl + '/checkout.html?order_id=' + orderId;
            }
            );
}

renderInventory();
renderOrderDetails();


// todo @jmphilli - block any interaction while waiting for server to respond / document new singleton order id
