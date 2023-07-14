let cart_popup = document.querySelector('.cart_popup');
let popup_open_btns = document.querySelectorAll('.popup_open');
let popup_close = document.querySelector('.popup_close');

let html_body = document.getElementsByTagName('body')[0];

function close_popup() {
    cart_popup.classList.remove('active');
    html_body.classList.remove('body_popup');
}

function uuidv4() {
    return ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g, c =>
      (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
    );
}

popup_open_btns.forEach((button) => {
    button.addEventListener('click', (e) => {
        e.preventDefault();
        cart_popup.classList.add('active');
        html_body.classList.add('body_popup');

        let closest_tr = button.closest(".product-tr");
        let title = closest_tr.querySelector('.product-title').textContent;
        let cost = closest_tr.querySelector('.product-cost').textContent;

        document.querySelector('.product_name').innerText = title;
        document.querySelector('.price_span').innerText = cost;
    })
});

popup_close.addEventListener('click',() => {
    close_popup();
});

// обработка кнопки добавления товара в корзину
document.querySelector('.cart_add_btn').addEventListener('click', (e) => {
    let title = document.querySelector('.product_name').textContent;
    let cost = document.querySelector('.price_span').textContent;

    let cart_object = JSON.parse(
        localStorage.getItem('cart')
    );
    if (cart_object == null) cart_object = {};

    cart_object[uuidv4()] = {
        'title': title,
        'cost': cost
    };
    localStorage.setItem('cart', JSON.stringify(cart_object));

    close_popup();
});