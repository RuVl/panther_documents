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

let cart_object = JSON.parse(localStorage.getItem("cart"));

let item_template = `
<div class="product_item">
    <span style="display: none" id="{0}"></span>
    <div class="name_div">{1}</div>
    <div class="quantity_div">
      <div class="counter_ co_mi"><i class="fa-solid fa-minus"></i></div>
      <div class="quantity">{2}</div>
      <div class="counter_ co_pl"><i class="fa-solid fa-plus"></i></div>
    </div>
    <div class="price_div">{3}</div>
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
    let cost = parseInt(cart_object[product_id].cost);
    let count = parseInt(cart_object[product_id].count);
    total_price += cost * count;
  }
  return total_price;
}

function close_popup() {
  pay_popup.classList.remove("active");
  html_body.classList.remove("body_popup");
}
// -----------------

if (cart_object != null && Object.keys(cart_object).length !== 0) {
  cart_page_wrap_div.classList.remove("inactive");
  for (let product_id in cart_object) {
    product_list_div.innerHTML += item_template.format(
      product_id,
      cart_object[product_id].title,
      cart_object[product_id].count,
      cart_object[product_id].cost
    );
  }
  final_price.textContent = evaluatePrice().toString();

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

      final_price.textContent = evaluatePrice().toString();

      if (Object.keys(cart_object).length === 0) {
        cart_page_wrap_div.classList.add("inactive");
        empty_cart_div.classList.remove("inactive");
      }
    });
  });

  // minus button handler
  let minus_btns = document.querySelectorAll('.co_mi');
  minus_btns.forEach((btn) => {
    btn.addEventListener("click", (e) => {
      let quantity_div = btn.closest(".quantity_div");
      let quantity = quantity_div.querySelector('.quantity');
      let product_div = btn.closest(".product_item");
      let product_id = product_div.getElementsByTagName("span")[0].id;

      let current_count = parseInt(quantity.textContent);
      if (current_count <= 1) {
        current_count = 1;
      } else {
        current_count--;
      }
      quantity.textContent = current_count;

      cart_object[product_id].count = current_count;
      localStorage.setItem("cart", JSON.stringify(cart_object));

      final_price.textContent = evaluatePrice().toString();
    });
  });

  // plus button handler
  let plus_btns = document.querySelectorAll('.co_pl');
  plus_btns.forEach((btn) => {
    btn.addEventListener("click", (e) => {
      let quantity_div = btn.closest(".quantity_div");
      let quantity = quantity_div.querySelector('.quantity');
      let product_div = btn.closest(".product_item");
      let product_id = product_div.getElementsByTagName("span")[0].id;

      let current_count = parseInt(quantity.textContent);
      if (current_count >= cart_object[product_id].max_count) {
        current_count = cart_object[product_id].max_count;
        alert(`${current_count} is maximum quantity of this item.`);
      } else {
        current_count++;
      }
      quantity.textContent = current_count;

      cart_object[product_id].count = current_count;
      localStorage.setItem("cart", JSON.stringify(cart_object));

      final_price.textContent = evaluatePrice().toString();
    });
  });

} else {
  empty_cart_div.classList.remove("inactive");
}

cart_pay_btn.onclick = () => {
  pay_popup.classList.add("active");
  html_body.classList.add("body_popup");
}

popup_close.onclick = close_popup;

function send_pay_form() {
  let cart = JSON.parse(localStorage.getItem("cart"));
  let pay_form = document.getElementById("pay_form");
  let formData = new FormData(pay_form);

  for (let product_id in cart) {
    formData.append('products', product_id);
  }

  fetch(pay_form.action, {
    body: formData,
    method: 'POST'
  })
  .then(resp => resp.json())
  .then(data => {
    console.log(data);
    document.querySelector('.alert > ul').innerHTML = '';
    if (!data.success) {
      for (let error in data.errors) {
        console.error(error, data.errors[error]);
        for (let err of data.errors[error]) {
          document.querySelector('.alert > ul').innerHTML += `
          <li>${error} : ${err}</li>
          `;
        }
      }
    } else {
      localStorage.removeItem('cart');
      window.location.replace(data['success_url']);
    }
  });
}
