document.addEventListener("DOMContentLoaded", function () {
  // 이미지 추가 창 출력
  const addBtn = document.querySelector(".add_btns");
  const insertForm = document.querySelector(".insert_form");
  addBtn.addEventListener("click", function () {
    if (insertForm.style.display === "flex") {
      insertForm.style.display = "none";
    } else {
      insertForm.style.display = "flex";
    }
  });

  const insertInput = document.querySelector(".insert_form_file");
  const insertSubmit = document.querySelector(".insert_form_btn");

  insertInput.addEventListener("change", () => {
    if (insertInput.files.length === 0) {
      insertSubmit.setAttribute("disabled", true);
    } else {
      insertSubmit.removeAttribute("disabled");
    }
  });

  // 이미지 업데이트 창 출력
  const updateBtn = document.querySelector(".update_btn");
  const updateForm = document.querySelector(".update_form");
  updateBtn.addEventListener("click", () => {
    if (updateForm.style.display === "flex") {
      updateForm.style.display = "none";
    } else {
      updateForm.style.display = "flex";
    }
  });

  // 모달 창 출력
  const thumbnails = document.querySelectorAll(".thumbnail");
  const modal = document.querySelector(".des_modal");
  const closeBtn = document.querySelector(".close_btn");
  const container = document.querySelector(".container");
  const deleteBtn = document.querySelector(".delete_btn");

  thumbnails.forEach((thumbnail, index) => {
    thumbnail.addEventListener("click", function () {
      const imageData = images[index];
      document.querySelector(".mimage").src =
        this.querySelector(".thumbnail_img").src;
      document.querySelector(".mfilename").textContent = imageData.filename;
      document.querySelector(".mfliecdate").textContent = imageData.upload_date;
      document.querySelector(".mfilesize").textContent =
        imageData.filesize + " bytes";
      document.querySelector(".mfileid").textContent = imageData.file_id;
      document.querySelector(".origin_id").value = imageData.file_id;

      modal.style.display = "flex";
      container.classList.add("blur-background");

      const updateInput = document.querySelector(".update_form_file");
      const updateSubmit = document.querySelector(".update_form_btn");

      updateInput.addEventListener("change", () => {
        if (updateInput.files.length === 0) {
          updateSubmit.setAttribute("disabled", true);
        } else {
          updateSubmit.removeAttribute("disabled");
        }
      });
      // 이미지 삭제 JS
      deleteBtn.replaceWith(deleteBtn.cloneNode(true));
      document.querySelector(".delete_btn").addEventListener("click", () => {
        location.href = "/imageserver/delete/" + imageData.file_id;
      });
    });
  });

  closeBtn.addEventListener("click", function () {
    modal.style.display = "none";
    container.classList.remove("blur-background");
  });
});
