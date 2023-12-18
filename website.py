import os
from flask import Flask, render_template, request, redirect, url_for, abort
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
        tempPath = userId + str(currentTime)

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

    # 将文件夹内的数据上传到服务器并清空文件夹
    # filenames = os.listdir(os.path.join(app.config['UPLOAD_PATH'], tempPath))
    # for filename in filenames:
    #     local_file_path = os.path.join(app.config['UPLOAD_PATH'], tempPath, filename)
    #     remote_file_path = "learn/cell/" + tempPath + "/"
    #     ssh_scp_put("192.168.175.128", 22, "zz", "xiaozhuzhen",
    #     local_file_path, remote_file_path, filename)

        # os.remove(os.path.join(app.config['UPLOAD_PATH'], tempPath, filename))

    # 删除这个空文件夹
    # os.rmdir(os.path.join(app.config['UPLOAD_PATH'], tempPath))

    # 从服务器上下载数据
    # local_dir_name = os.path.join("./downloads/" + tempPath)
    # check_file_path(local_dir_name)
    # down_from_remote(remote_dir_name=remote_file_path, local_dir_name=local_dir_name)

    return redirect(url_for("upload"))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
