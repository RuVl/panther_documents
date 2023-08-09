// Cart counter
window.addEventListener('DOMContentLoaded', () => {
    let cart_counter = document.querySelector('.cart_counter');
    let cart_object = JSON.parse(localStorage.getItem('cart'));
    if (cart_object != null)
        cart_counter.innerText = Object.keys(cart_object).length;
});

let burger_menu = document.querySelector('.burger_menu');
let vertical_menu = document.querySelector('.vertical_menu');

burger_menu.onclick = () => {
    vertical_menu.classList.toggle('hide_element_mobile');
}