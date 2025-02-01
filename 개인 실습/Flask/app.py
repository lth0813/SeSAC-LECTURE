# flask 클래스를 import 한다
from flask import Flask

# flask 클래스를 인스턴스화한다
app = Flask(__name__)

# URL과 실행할 함수를 매핑한다
@app.route("/")
def index():
    return "Hello, FlaskBook!"