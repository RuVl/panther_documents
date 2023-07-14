let product_list_div = document.querySelector('.product_list');
let cart_counter = document.querySelector('.cart_counter');


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
// -----------------



if (cart_object != null) {
    for (let product_id in cart_object) {
        product_list_div.innerHTML += item_template.format(
            product_id,
            cart_object[product_id].title,
            cart_object[product_id].cost
        );
    }


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
        });
    });
};

