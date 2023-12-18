import os
from flask import Flask, render_template, request, redirect, url_for, abort, send_from_directory
from werkzeug.utils import secure_filename
import paramiko
from utils import ssh_scp_put, down_from_remote, check_file_path
import getpass
import time

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = 'nii.gz'
app.config['UPLOAD_PATH'] = 'uploads'


@app.route("/upload", methods=["POST", "GET"])
def upload():
    global remote_file_path
    if request.method == "GET":
        return render_template("upload.html")
    else:
        userId = getpass.getuser()
        currentTime = int(round(time.time() * 1000))
        upload_files = request.files.getlist('file')
        tempPath = userId

        # 本地创建临时存储数据的文件夹
        check_file_path(os.path.join(app.config['UPLOAD_PATH'], tempPath))

        # 判断网页上传的数据后缀是否符合要求并存储在临时文件夹
        for upload_file in upload_files:
            filename = secure_filename(upload_file.filename)
            if filename != "":
                file_ext = ".".join(filename.split(".")[-2:])
                if file_ext != app.config['UPLOAD_EXTENSIONS']:
                    abort(400)
                upload_file.save(os.path.join(app.config['UPLOAD_PATH'], tempPath, filename))

        return redirect(url_for("upload"))

# function for download
@app.route("/download/<username>/<filename>", methods=['GET'])
def download(username, filename):
    if request.method == 'GET':
        path = os.path.isfile(os.path.join(app.config['UPLOAD_PATH'], username, filename))
        if path:
            directory = os.path.join(app.config['UPLOAD_PATH'], username)

            return send_from_directory(directory, filename, as_attachment=True)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
