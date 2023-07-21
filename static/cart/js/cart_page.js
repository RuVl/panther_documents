let product_list_div = document.querySelector(".product_list");
let cart_counter = document.querySelector(".cart_counter");
let final_price = document.querySelector(".final_price");

let empty_cart_div = document.querySelector(".empty_cart");
let cart_page_wrap_div = document.querySelector(".cart_page_wrap");

// some popup variables
let pay_popup = document.querySelector(".popup");
let html_body = document.getElementsByTagName("body")[0];
let popup_close = document.querySelector(".popup_close");
let cart_pay_btn = document.querySelector(".cart_pay_btn");

let final_pay_btn = document.querySelector(".pay_btn");


let cart_object = JSON.parse(localStorage.getItem("cart"));

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

String.prototype.format = function () {
  let formatted = this;
  for (let i = 0; i < arguments.length; i++) {
    let regexp = new RegExp("\\{" + i + "\\}", "gi");
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

function close_popup() {
  pay_popup.classList.remove("active");
  html_body.classList.remove("body_popup");
}
// -----------------

if (cart_object != null && Object.keys(cart_object).length != 0) {
  cart_page_wrap_div.classList.remove("deactive");
  for (let product_id in cart_object) {
    product_list_div.innerHTML += item_template.format(
      product_id,
      cart_object[product_id].title,
      cart_object[product_id].cost
    );
  }
  final_price.textContent = evaluatePrice();

  let remove_btns = document.querySelectorAll(".remove_div_a");
  remove_btns.forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.preventDefault();
      let product_div = btn.closest(".product_item");
      let product_id = product_div.getElementsByTagName("span")[0].id;
      delete cart_object[product_id];
      localStorage.setItem("cart", JSON.stringify(cart_object));
      btn.closest(".product_item").remove();

      cart_counter.innerText = Object.keys(cart_object).length;

      final_price.textContent = evaluatePrice();

      if (Object.keys(cart_object).length == 0) {
        cart_page_wrap_div.classList.add("deactive");
        empty_cart_div.classList.remove("deactive");
      }
    });
  });
} else {
  empty_cart_div.classList.remove("deactive");
}

cart_pay_btn.addEventListener("click", (e) => {
  if (document.getElementById('auth_user_email')) {
    send_pay_form();
  } else {
    pay_popup.classList.add("active");
    html_body.classList.add("body_popup");
  }
});

popup_close.addEventListener("click", (e) => {
  close_popup();
});

function send_pay_form() {
  let cart = JSON.parse(localStorage.getItem("cart"));
  let pay_form = document.getElementById("pay_form");
  let formData = new FormData(pay_form);

  for (let product_id in cart) {
    formData.append('products', product_id);
  }

  fetch('/cart/', {
    body: formData,
    method: 'POST'
  })
  .then(resp => resp.json())
  .then(data => {
    console.log(data)
    document.querySelector('.alert > ul').innerHTML = '';
    if (data.success == false) {
      for (let errors of data.errors) {
        let error_type = errors[0];
        console.log(error_type, errors[1])
        for (let err of errors[1]) {
          document.querySelector('.alert > ul').innerHTML += `
          <li>${error_type} : ${err}</li>
          `;
        }
      }
    }
    if (data.success == true) {
      localStorage.removeItem('cart');
      window.location.href = data.success_url;
    }
  });
}
