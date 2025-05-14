document.addEventListener("DOMContentLoaded", function () {
  const editProfileBtn = document.getElementById("editProfileBtn");
  const username = document.getElementById("username");
  const email = document.getElementById("email");
  const about = document.getElementById("about");
  const telegram = document.getElementById("telegram");
  const vk = document.getElementById("vk");
  const avatar = document.getElementById("avatar");

  let isEditing = false;

  editProfileBtn.addEventListener("click", function () {
    if (!isEditing) {
      // Включаем режим редактирования
      isEditing = true;
      editProfileBtn.textContent = "Сохранить";

      // Делаем поля редактируемыми
      username.contentEditable = true;
      email.contentEditable = true;
      about.contentEditable = true;

      // Добавляем стили для редактируемых полей
      username.classList.add("editable");
      email.classList.add("editable");
      about.classList.add("editable");
    } else {
      // Выключаем режим редактирования и сохраняем изменения
      isEditing = false;
      editProfileBtn.textContent = "Редактировать профиль";

      // Отключаем редактирование
      username.contentEditable = false;
      email.contentEditable = false;
      about.contentEditable = false;

      // Убираем стили
      username.classList.remove("editable");
      email.classList.remove("editable");
      about.classList.remove("editable");

      // Здесь можно добавить код для сохранения данных на сервер
      //  C помощью fetch API
      /*
                fetch('/api/profile', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        username: username.textContent,
                        email: email.textContent,
                        about: about.textContent
                    })
                })
                .then(response => response.json())
                .then(data => {
                    console.log('Success:', data);
                })
                .catch((error) => {
                    console.error('Error:', error);
                });
                */

      console.log("Изменения сохранены (в консоль):", {
        username: username.textContent,
        email: email.textContent,
        about: about.textContent,
      });
    }
  });
});
