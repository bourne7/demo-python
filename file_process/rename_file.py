import hashlib
import os

# 在文件名前面加上需要的文字。
import re
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


# 遍历所有的文件。这里面排除了 "." 开头的文件
def get_all_files(path):
    for dirpath, dirnames, filenames in os.walk(path):
        for dir_name in dirnames:
            print(os.path.join(dirpath, dir_name))
        for pure_file_name in filenames:
            if pure_file_name[0] == ".":
                continue

            if re.match("\\d{4}-\\d{2}-\\d{2}_\\d{2}-\\d{2}-\\d{2}.*", pure_file_name):
                print("Formatted name: "+pure_file_name)
                continue
            full_file_name = os.path.join(dirpath, pure_file_name)
            print(pure_file_name)

            time_stamp = os.path.getmtime(full_file_name)
            local_time = time.localtime(time_stamp)
            str_time = time.strftime("%Y-%m-%d_%H-%M-%S", local_time)
            print(str_time)

            new_file_name = os.path.join(dirpath, str_time + "_" + pure_file_name)

            os.rename(full_file_name, new_file_name)
            print(new_file_name)
            print()


if __name__ == '__main__':
    print('start')
    # rename_order('', 'D:\1')
    # rename_md5(r'D:\1')
    get_all_files(r'/1')
