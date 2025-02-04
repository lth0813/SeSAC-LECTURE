from flask import Flask, render_template, flash, request, redirect, send_from_directory, url_for
import os
import datetime

app = Flask(__name__)
app.config["DEBUG"] = True
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
# 자신의 업로드 폴더에 맞춰서 경로 수정 필수
UPLOAD_FOLDER = "C:/Users/user/Desktop/강의 교안/개인 실습/flask_assignment/apps/upload"
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

# 파일 서버 구현
@app.route("/fileserver", methods=["GET","POST"], endpoint="server")
def file_server():
    upload_root = app.config["UPLOAD_FOLDER"]
    if request.method == "POST":
        file = request.files["file"]
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], file.filename))
        return redirect("/fileserver")
    files = get_file_list()
    return render_template("fileserver.html", upload_root = upload_root, files = files)

# 파일 서버에서 파일 삭제
@app.route("/fileserver/del/<filename>")
def file_server_del(filename):
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    os.remove(file_path)
    return redirect(url_for("server"))

# 파일 서버에서 파일 다운로드
@app.route("/fileserver/download/<filename>")
def file_server_download(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename, as_attachment = True)


# 업로드 폴더에 있는 파일 리스트 가져오기
def get_file_list():
    file_list = []
    for filename in os.listdir(UPLOAD_FOLDER):
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file_type = filename.split(".")
        file_type = file_type[-1]
        file_color = get_file_type(file_type)
        if os.path.isfile(file_path):
            file_info = {
                "color" : file_color,
                "type" : file_type,
                "name" : filename,
                "size" : os.path.getsize(file_path),
                "created" : datetime.datetime.fromtimestamp(os.path.getctime(file_path)).strftime('%Y-%m-%d'),
                "updated" : datetime.datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d'),
            }
            file_list.append(file_info)
    return file_list

# 파일의 확장자로 파일 유형 구분하기
def get_file_type(type):
    image_exts = {"jpg", "jpeg", "png", "gif", "bmp", "webp", "svg"}
    text_exts = {"txt", "csv", "log", "md"}
    archive_exts = {"zip", "rar", "7z", "tar", "gz"}
    executable_exts = {"exe", "msi", "bat", "sh", "jar", "app"}
    if type in image_exts:
        return "green"
    elif type in text_exts:
        return "gray"
    elif type in archive_exts:
        return "blue"
    elif type in executable_exts:
        return "yellow"
    else:
        return "red"
    
if __name__ == "__main__":
    app.run(debug=True)


