let pay_popup = document.querySelector(".popup");
let html_body = document.getElementsByTagName("body")[0];
let popup_close = document.querySelector(".popup_close");
let cart_pay_btn = document.querySelector(".cart_pay_btn");

cart_pay_btn.onclick = () => {
  pay_popup.classList.add("active");
  html_body.classList.add("body_popup");
}

popup_close.onclick = () => {
  pay_popup.classList.remove("active");
  html_body.classList.remove("body_popup");
}

function send_pay_form(pay_form) {
  let cart = JSON.parse(localStorage.getItem("cart"));
  let formData = new FormData(pay_form);

  // Hidden products field widget
  for (let product_id in cart)
    formData.append('products', product_id);

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
          document.querySelector('.alert > ul').append(
            ...data.errors[error].map(err => Object.assign(document.createElement('li'), {textContent: `${error} : ${err}`}))
          );
        }
      } else {
        localStorage.removeItem("cart");
        window.location.assign(data['success_url']); // replace will clear document history
      }
    }).catch(reason => console.error(reason));
}