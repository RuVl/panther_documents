let product_data = {};

const cart_popup = document.querySelector('.popup');
function close_popup() {
    cart_popup.classList.remove('active');
    document.body.classList.remove('body_popup');
}

const cart_counter = document.querySelector('.cart_counter');
function add_to_cart() {
    let cart_object = JSON.parse(localStorage.getItem('cart'));
    if (cart_object == null) cart_object = {};

    cart_object[product_data.id] = {
        'title': product_data.title,
        'cost': product_data.cost,
        'count': 1,
        'max_count': product_data.max_count
    };
    localStorage.setItem('cart', JSON.stringify(cart_object));

    cart_counter.textContent = Object.keys(cart_object).length.toString();
}

document.querySelectorAll('.popup_open').forEach((button) => {
    button.addEventListener('click', (e) => {
        e.preventDefault();
        cart_popup.classList.add('active');
        document.body.classList.add('body_popup');

        let closest_tr = button.closest(".product-tr");
        let title = closest_tr.querySelector('.product-title').textContent;
        let cost = closest_tr.querySelector('.product-cost').textContent;

        document.querySelector('.product_name').textContent = title;
        document.querySelector('.price_span').textContent = cost;

        product_data.title = title;
        product_data.cost = cost;
        product_data.id = parseInt(closest_tr.querySelector('.product-id').textContent);
        product_data.max_count = parseInt(closest_tr.querySelector('.product-count').textContent);
    })
});

document.querySelector('.popup_close').addEventListener('click', close_popup);

// обработка кнопки добавления товара в корзину
document.querySelector('.cart_add_btn').addEventListener('click', () => {
    add_to_cart();
    close_popup();
});

document.querySelector('.pay_btn').addEventListener('click', () => {
    add_to_cart();
    window.location.assign(window.location.origin + '/cart');
});