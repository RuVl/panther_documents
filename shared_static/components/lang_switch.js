const form_input = document.getElementById('lang-picker');
const selected = document.querySelector(".lang-selected");

const optionsContainer = document.querySelector(".options-container");
const optionsList = document.querySelectorAll(".option");

selected.addEventListener("click", () => {
  optionsContainer.classList.toggle("active");
});

optionsList.forEach(el => {
  el.addEventListener("click", () => {
    selected.textContent = el.querySelector("label").textContent;
    optionsContainer.classList.remove("active");
    form_input.value = el.querySelector('input').value;
    form_input.form.submit();
  });
});