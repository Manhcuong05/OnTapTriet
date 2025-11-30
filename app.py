from flask import Flask, render_template, request, redirect, url_for, session
from questions import questions

app = Flask(__name__, static_folder="static")

# BẮT BUỘC phải có để dùng session
app.secret_key = "my-secret-key-123"  


@app.route("/")
def index():
    # Reset session khi vào trang chủ
    session["wrong"] = 0
    return render_template("index.html", total=len(questions))


@app.route("/quiz/<int:q_id>", methods=["GET", "POST"])
def quiz(q_id):

    # Nếu user mới vào quiz hoặc refresh → đảm bảo tồn tại biến session
    if "wrong" not in session:
        session["wrong"] = 0

    # Sai quá giới hạn (optional) → reset quiz
    if q_id > len(questions):
        return redirect(url_for("finish"))

    question = questions[q_id - 1]

    if request.method == "POST":
        user_answer = request.form.get("answer")
        correct = (user_answer == question["answer"])

        if not correct:
            session["wrong"] += 1  # tăng số câu sai

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
    wrong = session.get("wrong", 0)

    return f"""
    <h1>Bạn đã hoàn thành Quiz!</h1>
    <p>Số câu sai: {wrong}</p>
    <a href='/'>Làm lại</a>
    """


if __name__ == "__main__":
    app.run(debug=True)
