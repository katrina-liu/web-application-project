
function displayError(message) {
    let errorElement = document.getElementById("error")
    errorElement.innerHTML = message
}

function sanitize(s) {
    // Be sure to replace ampersand first
    return s.replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
}

function getCSRFToken() {
    let cookies = document.cookie.split(";")
    for (let i = 0; i < cookies.length; i++) {
        let c = cookies[i].trim()
        if (c.startsWith("csrftoken=")) {
            return c.substring("csrftoken=".length, c.length)
        }
    }
    return "unknown"
}

function nav_drop_down(){
    document.getElementById("id_dropdown_content").classList.toggle("show");
}

function toggle(source) {
    checkboxes = document.getElementsByName('available_product');
     for(var i=0, n=checkboxes.length;i<n;i++) {
    checkboxes[i].checked = source.checked;
  }
     selectProduct();
}


function selectProduct() {
    checkboxes = document.getElementsByName('available_product');
    var totalPrice = 0;
    for(var i=0, n=checkboxes.length;i<n;i++) {
        if (checkboxes[i].checked === true){
            totalPrice += parseInt((checkboxes[i]).value);
        }
    }
    var price = document.getElementById("id_total_price")
    price.innerText= totalPrice
}

