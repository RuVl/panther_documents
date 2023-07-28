window.onload = (e) => {
    let cart_counter = document.querySelector('.cart_counter');

    let cart_object = JSON.parse(
        localStorage.getItem('cart')
    );
    if (cart_object != null) {
        let i = Object.keys(cart_object).length;
        cart_counter.innerText = i;
    }
};