import json
import os


# 遍历所有的文件。这里面排除了 "." 开头的文件
def get_all_files(root_path, file_dict):
    for dir_file in os.listdir(root_path):
        # 这里要处理一下路径，原因是传到下一级的时候也需要只保持最右边的目录级别。
        path_elements = root_path.split(os.sep)
        root_dir_key_name = path_elements[path_elements.__len__() - 1]

        # 获取目录或者文件的路径
        dir_file_path = os.path.join(root_path, dir_file)

        # 判断该路径为文件还是路径
        if os.path.isdir(dir_file_path):
            if root_dir_key_name not in file_dict.keys():
                file_dict[root_dir_key_name] = {}
            # print(dir_file)
            file_dict[root_dir_key_name][dir_file] = {}
            get_all_files(dir_file_path, file_dict[root_dir_key_name])

        # 判断该路径为文件还是路径
        if os.path.isfile(dir_file_path):
            if root_dir_key_name not in file_dict.keys():
                file_dict[root_dir_key_name] = {}
            # print(dir_file)
            file_dict[root_dir_key_name][dir_file] = 'file'


# 扁平化一棵树
def flat_tree(root_path, file_dict, flat_content):
    for key in file_dict:
        # 获取目录或者文件的路径
        dir_file_path = os.path.join(root_path, key)
        # 将文件添加到扁平化的数据里面去
        flat_content = flat_content + dir_file_path + os.linesep
        if os.path.isdir(dir_file_path):
            flat_content = flat_tree(dir_file_path, file_dict[key], flat_content)
    return flat_content


if __name__ == '__main__':
    file_dict = {}
    get_all_files(r'article', file_dict)
    # content = json.dumps(file_dict, indent=2, ensure_ascii=False)
    # print(content)
    flat_content = ''
    print(flat_tree(r'', file_dict, flat_content))
