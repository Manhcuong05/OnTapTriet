from flask import Flask, render_template, request, redirect, url_for
from questions import questions
import os

# Khởi tạo Flask
app = Flask(__name__, static_folder="static")


@app.route("/")
def index():
    print("Loading index.html...")
    return render_template("index.html", total=len(questions))


@app.route("/quiz/<int:q_id>", methods=["GET", "POST"])
def quiz(q_id):
    if q_id > len(questions):
        return redirect(url_for("finish"))

    question = questions[q_id - 1]

    if request.method == "POST":
        user_answer = request.form.get("answer")
        correct = (user_answer == question["answer"])

        return render_template(
            "result.html",
            question=question,
            user_answer=user_answer,
            correct=correct,
            next_id=q_id + 1
        )

    return render_template("quiz.html", question=question)


@app.route("/finish")
def finish():
    return "<h1>Bạn đã hoàn thành Quiz!</h1> <a href='/'>Làm lại</a>"


# ---------------------------
#  Chạy server theo chuẩn Render
# ---------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
