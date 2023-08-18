const pay_popup = document.querySelector(".popup");

document.querySelector(".cart_pay_btn").onclick = () => {
  pay_popup.classList.add("active");
  document.body.classList.add("body_popup");
}

document.querySelector(".popup_close").onclick = () => {
  pay_popup.classList.remove("active");
  document.body.classList.remove("body_popup");
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
        window.location.assign(window.location.origin + data['success_url']); // replace will clear document history
      }
    }).catch(reason => console.error(reason));
}