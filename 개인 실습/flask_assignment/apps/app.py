from flask import Flask, render_template, flash, request, redirect, send_from_directory
import os

app = Flask(__name__)
app.secret_key = "lth0813"

# 과제 1
@app.route("/mp1/<username>")
def mp1(username):
    if len(username) % 2 == 0:
        username = username.upper()
    else:
        username = username.lower()
    return render_template("mp1.html", username = username)

# 과제 2
# POST 서버
@app.route("/mp2", methods=["GET","POST"])
def mp2_post():
    if request.method == "POST":
        number = request.form["number"]
        if number.isdigit():
            return redirect(f"/mp2/{number}")
        else:
            flash("숫자를 입력해주세요")
            return redirect("/mp2")
    else:
        return render_template("mp2.html")

# GET 서버
@app.route("/mp2/<number>")
def mp2_get(number):
    number = int(number)
    return render_template("mp2.html", number = number)

# 과제 3
# 업로드 폴더 만들기
UPLOAD_FOLDER = "upload"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# 업로드
@app.route("/mp3", methods=["GET","POST"])
def mp3_upload():
    if request.method == "POST":
        file = request.files["file"]
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], file.filename))
        return render_template("mp3.html", filename = file.filename)
    return render_template("mp3.html")

# 다운로드
@app.route("/download/<filename>")
def mp3_download(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename, as_attachment = True)


if __name__ == "__main__":
    app.run(debug=True)


