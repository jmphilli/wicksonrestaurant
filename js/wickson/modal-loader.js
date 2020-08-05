function loadMainPageModal() {
    var node = document.querySelector('#covid-modal');
    if (node != null && node !== undefined) {
        node.style.display = "block";
    } else {
        return;
    }
    var body = document.querySelector('#body');
    body.style.overflow = 'hidden';
    var elementId = '#close-covid-modal';
    var span = document.querySelector(elementId);
    if (span != null && span !== undefined) {
        span.onclick = function () {
            escapeHandler('#covid-modal');
            body.style.overflow = 'scroll';
        };
    }
}

function loadOrderModalHandler() {
    var node = document.querySelector('#order-link');
    if (node != null && node !== undefined) {
        node.onclick = function () {
            var orderModal = document.querySelector('#order-modal');
            orderModal.style.display = "block";
        };
    }
    var elementId = "#close-order-modal";
    var span = document.querySelector(elementId);
    if (span != null && span !== undefined) {
        span.onclick = function () {
            escapeHandler('#order-modal');
        };
    }
}

function escapeHandler(elementId) {
    var node = document.querySelector(elementId);
    if (node != null && node !== undefined) {
        node.style.display = "none";
    }
}

$(document).keyup(function(e) {
    if(e.key === "Escape") {
        escapeHandler('#covid-modal');
        escapeHandler('#order-modal'); // lol oops gotta do both
        var body = document.querySelector('#body');
        if (body != null && body !== undefined) {
            body.style.overflow = 'scroll';
        }
    }
});

loadMainPageModal();
loadOrderModalHandler();
