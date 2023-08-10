// Cart counter
window.addEventListener('DOMContentLoaded', () => {
    const cart_object = JSON.parse(localStorage.getItem('cart'));
    if (cart_object != null) {
        document.querySelectorAll('.cart_counter').forEach(el => el.innerText = Object.keys(cart_object).length);
    }

    const vertical_menu = document.getElementById('header-menu');
    document.getElementById('menu-control').firstElementChild.onclick = () => {
        vertical_menu.classList.toggle('hide_element_mobile');
    };
});