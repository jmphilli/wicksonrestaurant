// make a request to get every item and return the items
var siteUrl = 'http://wicksonrestaurant.com:8080';  // staging
// var siteUrl = 'https://wicksonrestaurant.com';  // prod
function parseInventoryItem(item) {
    return {
        id: item.id,
        name: item.name,
        price: (item.price/100).toFixed(2),
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

function buildHtmlInventory(inventory) {
    var htmlString = '';
    inventory.forEach(function (inventoryItem) {
        htmlString += `<div inventory_id="${inventoryItem.id}">${inventoryItem.name} -- \$ ${inventoryItem.price}</div><button onclick="addToCart('${inventoryItem.id}')">Add</button>`;
    });
    return htmlString;
}

function _render() {
    return getInventory().then(inventory => buildHtmlInventory(inventory));
}

function renderInventory() {
    var node = document.querySelector('#inventory');
    _render().then(htmlString => node.innerHTML = htmlString);
}

function getOrderId() {
    var node = document.querySelector('#order_id');
    return node.innerHTML;
}

function setOrderId(orderId) {
    var node = document.querySelector('#order_id');
    node.innerHTML = orderId;
}

function addToCart(inventoryId) {
    var orderId = getOrderId();
    console.log('order id is ' + orderId);
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
            setOrderId(order_id)
    });
}

renderInventory();
