import os
import paramiko


# 检测不出.nii.gz文件
# def validate_image(stream):
#     header = stream.read(512)
#     stream.seek(0)
#     format = imghdr.what(None, header)
#     if not format:
#         return None
#     return format

# python连接远程服务器，发送文件
def ssh_scp_put(ip, port, user, password, local_file, remote_dir, filename):
    """
    :param ip: 服务器ip地址
    :param port: 端口(22)
    :param user: 用户名
    :param password: 用户密码
    :param local_file: 本地文件地址
    :param remote_file: 要上传的文件地址（例：/test.txt）
    :return:
    """
    t = paramiko.Transport(sock=(ip, port))

    try:
        # 连接到远程服务器
        t.connect(username=user, password=password)
        # 使用 SFTP 协议创建一个传输通道
        sftp = paramiko.SFTPClient.from_transport(t)
        # 判断文件夹是否存在, 不存在则创建文件夹
        try:
            sftp.stat(remote_dir)
        except IOError:
            sftp.mkdir(remote_dir)
        # 上传本地文件到远程服务器
        remote_file = os.path.join(remote_dir, filename)
        sftp.put(local_file, remote_file)
        print(f"文件 {local_file} 已成功上传到 {remote_dir}")

    except Exception as e:
        print(f"上传文件时发生错误: {e}")

    finally:
        # 关闭 SSH 连接
        t.close()



def down_from_remote(ip="192.168.175.128", port=22, user="zz", password="xiaozhuzhen", remote_dir_name="learn/cell",
                     local_dir_name="./downloads"):
    t = paramiko.Transport(sock=(ip, port))

    # 远程下载文件
    try:
        t.connect(username=user, password=password)
        sftp = paramiko.SFTPClient.from_transport(t)
        remote_file = sftp.listdir(remote_dir_name)

        print('开始下载文件夹：' + remote_dir_name)
        for remote_file_name in remote_file:
            sub_remote = os.path.join(remote_dir_name, remote_file_name)
            sub_remote = sub_remote.replace('\\', '/')
            sub_local = os.path.join(local_dir_name, remote_file_name)
            sub_local = sub_local.replace('\\', '/')
            sftp.get(sub_remote, sub_local)

    except Exception as e:
        print(f"下载文件时发生错误: {e}")

    finally:

        t.close()


def check_file_path(path):
    if not os.path.exists(path):
        os.makedirs(path)
    return
