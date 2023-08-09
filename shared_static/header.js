// Cart counter
window.addEventListener('DOMContentLoaded', () => {
    let cart_counter = document.querySelector('.cart_counter');
    let cart_object = JSON.parse(localStorage.getItem('cart'));
    if (cart_object != null)
        cart_counter.innerText = Object.keys(cart_object).length;
})