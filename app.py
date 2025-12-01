from flask import Flask, render_template, request, redirect, url_for, session
from questions import questions
import os

app = Flask(__name__, static_folder="static")

# BẮT BUỘC để session hoạt động
app.secret_key = "my-secret-key-123"


@app.route("/")
def index():
    # Reset điểm khi bắt đầu lại quiz
    session["correct"] = 0
    session["wrong"] = 0
    return render_template("index.html", total=len(questions))


@app.route("/quiz/<int:q_id>", methods=["GET", "POST"])
def quiz(q_id):

    # Nếu vượt quá câu cuối → finish
    if q_id > len(questions):
        return redirect(url_for("finish"))

    # Nếu session chưa tồn tại thì tạo mới
    if "correct" not in session:
        session["correct"] = 0
    if "wrong" not in session:
        session["wrong"] = 0

    question = questions[q_id - 1]

    # User gửi đáp án
    if request.method == "POST":
        user_answer = request.form.get("answer")
        correct = (user_answer == question["answer"])

        if correct:
            session["correct"] += 1
        else:
            session["wrong"] += 1

        # Trả về lại trang quiz với UI đúng/sai
        return render_template(
            "quiz.html",
            question=question,
            q_id=q_id,
            question_list=list(range(1, len(questions) + 1)),
            answered=True,
            user_answer=user_answer,
            correct=correct
        )

    # GET → hiển thị câu hỏi bình thường
    return render_template(
        "quiz.html",
        question=question,
        q_id=q_id,
        question_list=list(range(1, len(questions) + 1)),
        answered=False
    )


@app.route("/finish")
def finish():
    correct = session.get("correct", 0)
    wrong = session.get("wrong", 0)
    total = len(questions)

    return render_template(
        "finish.html",
        correct=correct,
        wrong=wrong,
        total=total
    )


if __name__ == "__main__":
    # Cấu hình chuẩn cho Render / local
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
