const form_input = document.getElementById('lang-picker');
const selected = document.querySelector(".lang-selected");

const lang_select = document.querySelector(".lang-select");
const optionsList = document.querySelectorAll(".option");

selected.addEventListener("click", () => {
  lang_select.classList.toggle("active");
});

optionsList.forEach(el => {
  el.addEventListener("click", () => {
    selected.querySelector('span').textContent = el.querySelector("label").textContent;
    lang_select.classList.remove("active");
    form_input.value = el.querySelector('input').value;
    form_input.form.submit();
  });
});