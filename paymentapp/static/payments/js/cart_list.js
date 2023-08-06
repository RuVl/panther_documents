let product_list_div = document.querySelector(".product_list");
let cart_counter = document.querySelector(".cart_counter");
let final_price = document.querySelector(".final_price");

let empty_cart_div = document.querySelector(".empty_cart");
let cart_page_wrap_div = document.querySelector(".cart_page_wrap");

let cart_object = JSON.parse(localStorage.getItem("cart"));

function get_item_html(product_id) {
	let cart = cart_object[product_id];
	// noinspection HtmlUnknownAttribute
	return `
  <div class="product_item" product-id="${product_id}">
		<div class="name_div">${cart.title}</div>
		<div class="quantity_div">
      <div class="counter_ co_mi ${cart.count === 1 ? 'disabled' : ''}" onclick="counter_change(this, 'minus')"><i class="fa-solid fa-minus"></i></div>
      <div class="quantity">${cart.count}</div>
      <div class="counter_ co_pl ${cart.count === cart.max_count ? 'disabled' : ''}" onclick="counter_change(this, 'plus')"><i class="fa-solid fa-plus"></i></div>
    </div>
    <div class="price_div">${cart.cost}</div>
    <div class="remove_div">
        <a href class="remove_div_a" onclick="return delete_product(this)">Удалить</a>
    </div>
	</div>`
}

function counter_change(btn, change) {
  if (btn.classList.contains("disabled"))
    return;

  let quantity = btn.parentElement.querySelector('.quantity');
  let product_id = btn.parentElement.parentElement.getAttribute("product-id");

  let current_count = parseInt(quantity.textContent);
  switch (change) {
    case 'minus':
      if (current_count > 2) {
        current_count--;
        btn.nextElementSibling.nextElementSibling.classList.remove("disabled");
      } else {
        current_count = 1;
        btn.classList.add("disabled");
      }
      break;
    case 'plus':
      if (current_count < cart_object[product_id].max_count - 1) {
        current_count++;
        btn.previousElementSibling.previousElementSibling.classList.remove("disabled");
      } else {
        current_count = cart_object[product_id].max_count;
        btn.classList.add("disabled");
      }
      break;
    default:
      return;
  }
  quantity.textContent = current_count.toString();

  cart_object[product_id].count = current_count;
  localStorage.setItem("cart", JSON.stringify(cart_object));

  final_price.textContent = evaluatePrice().toString();
}

function delete_product(btn) {
  let product_item = btn.parentElement.parentElement;
  let product_id = product_item.getAttribute("product-id");
  delete cart_object[product_id];

  localStorage.setItem("cart", JSON.stringify(cart_object));
  product_item.remove();

  cart_counter.innerText = Object.keys(cart_object).length;

  final_price.textContent = evaluatePrice().toString();

  if (Object.keys(cart_object).length === 0) {
    cart_page_wrap_div.classList.add("inactive");
    empty_cart_div.classList.remove("inactive");
  }

  return false; // event.preventDefault
}

function evaluatePrice() {
  let total_price = 0;
  for (let product_id in cart_object) {
    let cost = parseInt(cart_object[product_id].cost);
    let count = parseInt(cart_object[product_id].count);
    total_price += cost * count;
  }
  return total_price;
}

if (cart_object != null && Object.keys(cart_object).length !== 0) {
  cart_page_wrap_div.classList.remove("inactive");
  for (let product_id in cart_object)
    product_list_div.innerHTML += get_item_html(product_id);

  final_price.textContent = evaluatePrice().toString();
} else {
  empty_cart_div.classList.remove("inactive");
}
