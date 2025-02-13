from flask import *
from pymongo import MongoClient
import gridfs
import os
from bson import ObjectId
import io
import subprocess
import imghdr

class HandleImage():
    def __init__(self, db_name="image_db", collection_name="fs"):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client[db_name]
        self.fs = gridfs.GridFS(self.db, collection=collection_name)
        subprocess.Popen(r' start cmd /k "mongod --dbpath C:/mongodb/dogs"', shell=True)

    def save_image(self, file):
        order = self.db.fs.files.count_documents({}) + 1
        file_id = self.fs.put(file.read(), filename = file.filename, metadata={"order": order})
        return str(file_id)
    
    def get_image(self):
        images = []
        for file in self.db.fs.files.find().sort("metadata.order"):
            images.append({
                "filename" : file["filename"],
                "upload_date" : file["uploadDate"].strftime('%Y-%m-%d'),
                "filesize" : file["length"],
                "file_id" : str(file["_id"])
            })
        return images
    
    def delete_image(self, file_id):
        file_id = ObjectId(file_id)
        self.fs.delete(file_id)

    def update_image(self, file_id, new_file):
        file_id = ObjectId(file_id)
        origin_file = self.db.fs.files.find_one({"_id": file_id})
        metadata = origin_file.get("metadata", {})
        with self.client.start_session() as session:
            with session.start_transaction():
                self.fs.delete(file_id)
                new_file_id = self.fs.put(new_file.read(), filename = new_file.filename, metadata = metadata, _id = file_id)
                return str(new_file_id)

app = Flask(__name__)
app.secret_key = os.urandom(24)
handler = HandleImage()

@app.route("/")
def initserver():
    return render_template("init.html")

@app.route("/imageserver")
def imagesever():
    images = handler.get_image()
    return render_template("imageserver.html", images = images)

@app.route("/imageserver/insert", methods=["POST"])
def insert_image():
    file = request.files["insert_file"]
    if file is None:
        flash("파일을 선택해주세요.")
        return redirect("/imageserver")
    handler.save_image(file)
    return redirect("/imageserver")

@app.route("/imageserver/get/<file_id>")
def image_get(file_id):
    file = handler.fs.get(ObjectId(file_id))
    file_data = file.read()
    img_type = imghdr.what(None, file_data)
    if img_type:
        mimetype = f"image/{img_type}"
    else:
        mimetype = "application/octet-stream"
    return send_file(io.BytesIO(file_data), mimetype=mimetype)

@app.route("/imageserver/update", methods=["POST"])
def update_image():
    file = request.files["update_file"]
    file_id = request.form.get("origin_id")
    handler.update_image(file_id, file)
    return redirect("/imageserver")

@app.route("/imageserver/delete/<file_id>")
def delete_image(file_id):
    handler.delete_image(file_id)
    return redirect("/imageserver")