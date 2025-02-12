from flask import *
from pymongo import MongoClient
import gridfs
import os
from bson import ObjectId
import io

class HandleImage():
    def __init__(self, db_name="image_db", collection_name="fs"):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client[db_name]
        self.fs = gridfs.GridFS(self.db, collection=collection_name)

    def save_image(self, file):
        file_id = self.fs.put(file.read(), filename = file.filename)
        return str(file_id)
    
    def get_image(self):
        images = []
        for file in self.db.fs.files.find():
            images.append({
                "filename" : file["filename"],
                "upload_date" : file["uploadDate"].strftime('%Y-%m-%d'),
                "filesize" : file["length"],
                "file_id" : str(file["_id"])
            })
        return images
    
    def delete_image(self, file_id):
        self.fs.delete(file_id)

    def update_image(self, file_id, new_file):
        self.delete_image(file_id)
        new_file_id = self.save_image(new_file)
        return str(new_file_id)

app = Flask(__name__)
app.secret_key = os.urandom(24)
handler = HandleImage()

@app.route("/imageserver")
def imagesever():
    images = handler.get_image()
    return render_template("imageserver.html", images = images)

@app.route("/imageserver/insert", methods=["POST"])
def insert_image():
    file = request.files["file"]
    handler.save_image(file)
    return redirect("/imageserver")

@app.route("/imageserver/get/<file_id>")
def image_get(file_id):
    file = handler.fs.get(ObjectId(file_id))
    return send_file(io.BytesIO(file.read()), mimetype="image/jpg")
