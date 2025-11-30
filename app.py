from flask import Flask, render_template, request, redirect, url_for, session
from questions import questions
import os

app = Flask(__name__, static_folder="static")
app.secret_key = "cuong-la-nhat"   # Secret key để dùng session


@app.route("/")
def index():
    # Reset điểm mỗi lần làm mới
    session["correct"] = 0
    session["wrong"] = 0
    return render_template("index.html", total=len(questions))


@app.route("/quiz/<int:q_id>", methods=["GET", "POST"])
def quiz(q_id):
    if q_id > len(questions):
        return redirect(url_for("finish"))

    question = questions[q_id - 1]

    if request.method == "POST":
        user_answer = request.form.get("answer")
        is_correct = (user_answer == question["answer"])

        if is_correct:
            session["correct"] += 1
        else:
            session["wrong"] += 1

        return render_template(
            "result.html",
            question=question,
            user_answer=user_answer,
            correct=is_correct,
            next_id=q_id + 1
        )

    return render_template("quiz.html", question=question)


@app.route("/finish")
def finish():
    correct = session.get("correct", 0)
    wrong = session.get("wrong", 0)
    total = correct + wrong

    return render_template("finish.html",
                           correct=correct,
                           wrong=wrong,
                           total=total)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
