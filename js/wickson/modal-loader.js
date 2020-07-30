function loadMainPageModal() {
    var node = document.querySelector('#covid-modal');
    if (node != null && node !== undefined) {
        node.style.display = "block";
    }
    var span = document.getElementsByClassName("close")[0];
    if (span != null && span !== undefined) {
        span.onclick = function () {
            escapeHandler()
        };
    }
}

function escapeHandler() {
    var node = document.querySelector('#covid-modal');
    if (node != null && node !== undefined) {
        node.style.display = "none";
    }
}

$(document).keyup(function(e) {
    if(e.key === "Escape") {
        escapeHandler(e);
    }
});

loadMainPageModal();
