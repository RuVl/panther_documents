// Данные о товарах из localStorage
const cart_object = JSON.parse(localStorage.getItem("cart"));

// Элементы корзины
const empty_cart_div = document.querySelector(".empty_cart");
const cart_page_wrap_div = document.querySelector(".cart_page_wrap");

function showProducts(products) {
  const product_list_div = document.querySelector(".product_list");
  Object.entries(products).forEach(([product_id, product]) => {
    product_list_div.appendChild(
      Object.assign(document.createElement('div'), {classList: 'product_item'})
    ).append(
      // Наименование
      Object.assign(document.createElement('div'), {classList: 'name_div'}).appendChild(
        Object.assign(document.createElement('span'), {textContent: product.title})
      ).parentElement,
      // Счётчик
      Object.assign(document.createElement('div'), {classList: 'quantity_div'}).appendChild(
        // Уменьшить
        Object.assign(document.createElement('div'), {classList: 'counter_ co_mi' + (product.count === 1 ? ' disabled' : ''), innerHTML: '<i class="fa-solid fa-minus"></i>'})
      ).parentElement.appendChild(
        // Количество
        Object.assign(document.createElement('div'), {classList: 'quantity', textContent: product.count})
      ).parentElement.appendChild(
        // Увеличить
        Object.assign(document.createElement('div'), {classList: 'counter_ co_pl' + (product.count === product.max_count ? ' disabled' : ''), innerHTML: '<i class="fa-solid fa-plus"></i>'})
      ).parentElement,
      // Стоимость 1 шт
      Object.assign(document.createElement('div'), {classList: 'price_div'}).appendChild(
        Object.assign(document.createElement('span'), {textContent: product.cost})
      ).parentElement
    );
    // Id продукта
    product_list_div.lastElementChild.setAttribute('product-id', product_id);
  });
  // События счётчика
  product_list_div.querySelectorAll('.counter_').forEach(el => el.addEventListener('click', counter_change));
  // Кнопка закрытия
  product_list_div.childNodes.forEach(el => el.insertAdjacentHTML(
    'beforeend', '<div class="remove_div"><span onclick="return delete_product(this)">Удалить</span></div>'
  ));
}

// Уменьшение количества товаров
function counter_change(_) {
  if (this.classList.contains("disabled"))
    return;

  let quantity = this.parentElement.querySelector('.quantity');
  let product_id = this.parentElement.parentElement.getAttribute("product-id");

  let current_count = parseInt(quantity.textContent);
  if (this.classList.contains('co_mi')) {
    if (current_count > 2) {
      current_count--;
      this.nextElementSibling.nextElementSibling.classList.remove("disabled");
    } else {
      current_count = 1;
      this.classList.add("disabled");
    }
  } else if (this.classList.contains('co_pl')) {
    if (current_count < cart_object[product_id].max_count - 1) {
      current_count++;
      this.previousElementSibling.previousElementSibling.classList.remove("disabled");
    } else {
      current_count = cart_object[product_id].max_count;
      this.classList.add("disabled");
    }
  } else return;
  quantity.textContent = current_count.toString();

  cart_object[product_id].count = current_count;
  localStorage.setItem("cart", JSON.stringify(cart_object));

  calcFinalPrice();
}

const cart_counter = document.querySelector(".cart_counter");
function delete_product(btn) {
  let product_item = btn.parentElement.parentElement;
  let product_id = product_item.getAttribute("product-id");
  delete cart_object[product_id];

  localStorage.setItem("cart", JSON.stringify(cart_object));
  product_item.remove();

  cart_counter.textContent = Object.keys(cart_object).length.toString();
  calcFinalPrice();

  if (Object.keys(cart_object).length === 0) {
    cart_page_wrap_div.classList.add("inactive");
    empty_cart_div.classList.remove("inactive");
  }

  return false; // event.preventDefault
}


const final_price = document.querySelector(".final_price");
function calcFinalPrice() {
  let total_price = 0;
  for (let product_id in cart_object) {
    let cost = parseInt(cart_object[product_id].cost);
    let count = parseInt(cart_object[product_id].count);
    total_price += cost * count;
  }
  final_price.textContent = total_price.toString();
}

window.addEventListener("DOMContentLoaded", () => { // Загружаем корзину как только весь DOM получен
  if (cart_object != null && Object.keys(cart_object).length !== 0) {
    cart_page_wrap_div.classList.remove("inactive");
    showProducts(cart_object);
    calcFinalPrice();
  } else empty_cart_div.classList.remove("inactive");
})