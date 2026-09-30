from flask import Flask, jsonify, request, render_template

from model import LogisticModel, LogisticModel2

app = Flask(__name__)


MODEL_FIELDS = {
    "model1": (
        "weeks",
        "premature_birth",
        "smokes",
        "adynamia",
        "smoothness",
        "wb_level",
        "bmi",
        "sti",
        "spotting",
    ),

    "model2": (
        "wb_level",
        "wb_avg_ep_avg_ratio",
        "abortion",
        "polycystic_ovary",
        "wb_count",
    ),
}


MODEL_CLASSES = {
    "model1": LogisticModel,
    "model2": LogisticModel2,
}

def read_answers(fields):
    answers = {}

    for field_name in fields:
        value = request.form.get(field_name)

        if value not in {"0", "1"}:
            raise ValueError(
                f"Поле {field_name} отсутствует или содержит неверное значение"
            )

        answers[field_name] = int(value)

    return answers

@app.route("/")
def index():
    questionnaires_links = {
    "Программа прогнозирования спонтанных преждевременных родов в I, II, и III триместрах беременности": 
        "premature_birth_questionnaire",
    "Программа прогнозирования спонтанных экстремально ранних преждевременных родов с выполнением расчета в I и II триместрах беременности":
        "extreme_premature_birth_questionnaire"
}
    print(questionnaires_links)
    return render_template("index.html", questionnaires_links=questionnaires_links)

@app.route("/questionnaires/premature-labor-questionnaire")
def premature_birth_questionnaire():
    return render_template("premature_labor_questionnaire.html")


@app.route("/questionnaires/extreme_premature_birth_questionnaire")
def extreme_premature_birth_questionnaire():
    return render_template("extreme_premature_birth_questionnaire.html")
    
    
@app.route("/submit", methods=["POST"])
def submit():
    try:
        model_name = request.form.get("model")

        if model_name not in MODEL_CLASSES:
            raise ValueError("Неизвестная модель")

        fields = MODEL_FIELDS[model_name]
        answers = read_answers(fields)

        model_class = MODEL_CLASSES[model_name]
        model = model_class(**answers)

        result = model.calculate()

    except ValueError as error:
        return jsonify(
            success=False,
            message=str(error)
        ), 400

    except Exception:
        app.logger.exception("Ошибка во время обработки анкеты")

        return jsonify(
            success=False,
            message="Не удалось выполнить расчёт"
        ), 500

    return jsonify(
        success=True,
        probability=result,
        percentage=round(result * 100, 2)
    )


if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=3000
    )