document.addEventListener("DOMContentLoaded", function () {
  const addBtn = document.querySelector(".add_btns");
  const insertForm = document.querySelector(".insert_form");

  addBtn.addEventListener("click", function () {
    if (insertForm.style.display === "flex") {
      insertForm.style.display = "none";
    } else {
      insertForm.style.display = "flex";
    }
  });
});
