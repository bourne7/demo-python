import hashlib
import os

# 在文件名前面加上需要的文字。
import shutil
import time


def add_before_name(pattern: str, path_src: str) -> None:
    i = 0
    for files in os.listdir(path_src):
        file_name_old = path_src + os.sep + files
        file_name_new = path_src + os.sep + pattern + '{0:0>4d}_'.format(i) + files.replace(' ', '_').lower()
        i += 1
        print(file_name_old + " -> " + file_name_new)
        os.rename(file_name_old, file_name_new)


# 格式化成为 字符+序号
def rename_order(pattern: str, path_src: str) -> None:
    i = 0
    for files in os.listdir(path_src):
        file_name_old = path_src + os.sep + files
        file_type = os.path.splitext(files)[1]
        file_name_new = path_src + os.sep + pattern + '{0:0>4d}'.format(i) + file_type.lower()
        i += 1
        print(file_name_old + " -> " + file_name_new)
        os.rename(file_name_old, file_name_new)


# md5 命名所有文件
def rename_md5(path_src: str) -> None:
    # 新建目录
    path_src_md5 = path_src + '_md5'
    print(path_src_md5)

    # 如果有存在目录就删除
    if os.path.exists(path_src_md5):
        shutil.rmtree(path_src_md5)

    time.sleep(.0000000000000001)
    os.mkdir(path_src_md5)

    i = 0
    for files in os.listdir(path_src):
        file_name_old = path_src + os.sep + files

        with open(file_name_old, 'rb') as f:
            md5 = hashlib.md5(f.read()).hexdigest()

            file_type = os.path.splitext(files)[1]
            file_name_new = path_src_md5 + os.sep + md5 + file_type
            i += 1
            print(file_name_old + " -> " + file_name_new)
            shutil.copyfile(file_name_old, file_name_new)


if __name__ == '__main__':
    print('start')
    # rename_order('', 'D:\1')
    rename_md5(r'D:\1')
