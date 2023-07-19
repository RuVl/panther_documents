let product_list_div = document.querySelector('.product_list');
let cart_counter = document.querySelector('.cart_counter');
let final_price = document.querySelector('.final_price');

let empty_cart_div = document.querySelector('.empty_cart');
let cart_page_wrap_div = document.querySelector('.cart_page_wrap');

let cart_object = JSON.parse(
    localStorage.getItem('cart')
);

let item_template = `
<div class="product_item">
    <span style="display: none" id="{0}"></span>
    <div class="name_div">{1}</div>
    <div class="quantity_div">1</div>
    <div class="price_div">{2}</div>
    <div class="remove_div">
        <a href class="remove_div_a">Удалить</a>
    </div>
</div>
`;

String.prototype.format = function() {
    let formatted = this;
    for (let i = 0; i < arguments.length; i++) {
      let regexp = new RegExp('\\{'+i+'\\}', 'gi');
      formatted = formatted.replace(regexp, arguments[i]);
    }
    return formatted;
};

function evaluatePrice() {
    let total_price = 0;
    for (let product_id in cart_object) {
        total_price += parseInt(cart_object[product_id].cost);
    }
    return total_price;
}
// -----------------



if (cart_object != null && Object.keys(cart_object).length != 0) {
    cart_page_wrap_div.classList.remove('deactive');
    for (let product_id in cart_object) {
        product_list_div.innerHTML += item_template.format(
            product_id,
            cart_object[product_id].title,
            cart_object[product_id].cost
        );
    }
    final_price.textContent = evaluatePrice();

    let remove_btns = document.querySelectorAll('.remove_div_a');
    remove_btns.forEach((btn) => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            let product_div = btn.closest('.product_item');
            let product_id = product_div.getElementsByTagName('span')[0].id;
            delete cart_object[product_id];
            localStorage.setItem(
                'cart',
                JSON.stringify(cart_object)
            );
            btn.closest('.product_item').remove();

            cart_counter.innerText =
                Object.keys(cart_object).length;
            
            final_price.textContent = evaluatePrice();

            if (Object.keys(cart_object).length == 0) {
                cart_page_wrap_div.classList.add('deactive');
                empty_cart_div.classList.remove('deactive');
            }
        });
    });
} else {
    empty_cart_div.classList.remove('deactive');
}

