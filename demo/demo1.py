import os


def get_latest_folder(directory):
    # 获取目录下所有的文件和文件夹
    entries = [os.path.join(directory, entry) for entry in os.listdir(directory)]
    # 过滤出所有文件夹
    folders = [entry for entry in entries if os.path.isdir(entry)]
    if not folders:
        return None
    # 按照文件夹的创建时间进行排序，并获取最新的文件夹
    latest_folder = max(folders, key=os.path.getctime)
    # 返回最新文件夹的名称

    return os.path.basename(latest_folder)


def check_vmdk_files(input_path):
    directory = os.path.join(input_path, get_latest_folder(input_path))
    # 检查目录是否存在
    if not os.path.isdir(directory):
        return False
    found_files = False
    # 遍历目录及其子目录中的文件
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.vmdk'):
                print(f"发现 .vmdk 文件: {os.path.join(root, filename)}")
                found_files = True
    if not found_files:
        print("没有找到 .vmdk 文件")
    return found_files

if __name__ == '__main__':
    path = r"M:\\测试最新目录"
    check_vmdk_files(path)