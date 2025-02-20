from flask import Flask, render_template, jsonify
import json

app = Flask(__name__)
app.config["DEBUG"] = True
app.secret_key = "lth0813"
JSON_FILE_PATH = "geojson.json"

@app.route("/")
def map():
    return render_template("map.html")

@app.route("/geo")
def geo():
    try:
        # JSON 파일 불러오기
        with open(JSON_FILE_PATH, encoding="utf-8") as f:
            data = json.load(f)
        return jsonify(data)  # JSON 응답 반환
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # 에러 처리
