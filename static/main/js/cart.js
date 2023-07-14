let cart_popup = document.querySelector('.cart_popup');
let popup_open_btns = document.querySelectorAll('.popup_open');
let popup_close = document.querySelector('.popup_close');

let html_body = document.getElementsByTagName('body')[0];

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
    cart_popup.classList.remove('active');
    html_body.classList.remove('body_popup');
});