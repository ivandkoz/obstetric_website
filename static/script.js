// Находим HTML-элементы, с которыми будем работать.
const form = document.querySelector("#survey-form");
const submitButton = document.querySelector("#submit-button");

const resultDialog = document.querySelector("#result-dialog");
const resultTitle = document.querySelector("#result-title");
const resultValue = document.querySelector("#result-value");
const resultMessage = document.querySelector("#result-message");

const closeIcon = document.querySelector("#dialog-close-icon");
const closeButton = document.querySelector("#dialog-close-button");
const resetButton = document.querySelector("#reset-button");


// Регистрируем функцию, которая будет вызвана при отправке формы.
form.addEventListener("submit", async function (event) {
    // Отменяем обычную отправку формы и переход на новую страницу.
    event.preventDefault();

    const originalButtonText = submitButton.textContent;

    submitButton.disabled = true;
    submitButton.textContent = "Выполняется расчёт...";

    try {
        // Собираем все значения полей формы.
        const formData = new FormData(form);

        // Отправляем POST-запрос во Flask.
        const response = await fetch(form.action, {
            method: "POST",
            body: formData
        });

        let data;

        try {
            // Преобразуем JSON-ответ сервера в JavaScript-объект.
            data = await response.json();
        } catch {
            throw new Error(
                "Сервер вернул ответ в неизвестном формате"
            );
        }

        // fetch не считает ответы 400 и 500 ошибкой автоматически,
        // поэтому проверяем response.ok самостоятельно.
        if (!response.ok || !data.success) {
            throw new Error(
                data.message || "Не удалось выполнить расчёт"
            );
        }

        showSuccessResult(data);

    } catch (error) {
        showErrorResult(error.message);

    } finally {
        // Этот код выполнится и при успехе, и при ошибке.
        submitButton.disabled = false;
        submitButton.textContent = originalButtonText;
    }
});


function showSuccessResult(data) {
    resultDialog.classList.remove("error");

    resultTitle.textContent = "Расчёт выполнен";

    const percentage = Number(data.percentage);

    resultValue.textContent =
        percentage.toFixed(2).replace(".", ",") + " %";

    resultMessage.textContent =
        `Ответы сохранены. Номер записи: ${data.response_id}.`;

    resultDialog.showModal();
}


function showErrorResult(message) {
    resultDialog.classList.add("error");

    resultTitle.textContent = "Произошла ошибка";
    resultValue.textContent = "";
    resultMessage.textContent = message;

    resultDialog.showModal();
}


// Закрытие окна по верхней кнопке ×.
closeIcon.addEventListener("click", function () {
    resultDialog.close();
});


// Закрытие окна по нижней кнопке.
closeButton.addEventListener("click", function () {
    resultDialog.close();
});


// Закрываем окно, очищаем форму и прокручиваем страницу вверх.
resetButton.addEventListener("click", function () {
    resultDialog.close();
    form.reset();

    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });
});