function nav_drop_down(){
    document.getElementById("id_dropdown_content").classList.toggle("show");
}

function toggle(source) {
    checkboxes = document.getElementsByName('available_product');
    for(var checkbox in checkboxes)
      checkbox.checked = source.checked;
}