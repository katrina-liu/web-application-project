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

