from flask import Flask, request, render_template

from model import LogisticModel


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    try:
        model = LogisticModel(
            weeks=int(request.form["weeks"]),
            premature_birth=int(request.form["premature_birth"]),
            smokes=int(request.form["smokes"]),
            adynamia=int(request.form["adynamia"]),
            smoothness=int(request.form["smoothness"]),
            wb_level=int(request.form["wb_level"]),
            bmi=int(request.form["bmi"]),
            sti=int(request.form["sti"]),
            spotting=int(request.form["spotting"])
        )
    except (KeyError, ValueError):
        return "Ошибка: проверьте правильность заполнения формы", 400

    result = model.calculate()

    return f"""
        <h1>Результат</h1>
        <p>Вероятность: {result:.2%}</p>
        <a href="/">Вернуться к форме</a>
    """


if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=3000
    )