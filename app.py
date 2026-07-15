from flask import Flask,jsonify, request, render_template

from model import LogisticModel
from database import init_database, save_response

app = Flask(__name__)

init_database()

BINARY_FIELDS = (
    "weeks",
    "premature_birth",
    "smokes",
    "adynamia",
    "smoothness",
    "wb_level",
    "bmi",
    "sti",
    "spotting",
)

def read_answers():
    """
    Transform answers in forms to binary data
    """

    answers = {}

    for field_name in BINARY_FIELDS:
        value = request.form.get(field_name)

        if value not in {"0", "1"}:
            raise ValueError(
                f"Поле {field_name} отсутствует или содержит неверное значение"
            )

        answers[field_name] = int(value)

    return answers

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    try:
        answers = read_answers()

        model = LogisticModel(**answers)
        result = model.calculate()

        response_id = save_response(
            answers=answers,
            probability=result
        )
        
    except ValueError as error:
        return jsonify(
            success=False,
            message=str(error)
        ), 400

    except Exception:

        app.logger.exception("Ошибка во время обработки анкеты")

        return jsonify(
            success=False,
            message="Не удалось выполнить расчёт или сохранить результат"
        ), 500

    return jsonify(
        success=True,
        probability=result,
        percentage=round(result * 100, 2),
        response_id=response_id
    )



if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=3000
    )