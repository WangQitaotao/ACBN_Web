import os
import random
import hashlib
from datetime import datetime


def generate_unique_file(filepath, size_mb):
    """生成一个指定大小（MB）的文件，并确保内容唯一"""
    size_bytes = size_mb * 1024 * 1024  # 将MB转换为字节
    with open(filepath, 'wb') as f:
        # 生成一个唯一的随机字节序列
        unique_content = os.urandom(size_bytes)
        f.write(unique_content)
    return filepath


def get_md5(filepath):
    """计算文件的MD5哈希"""
    hash_md5 = hashlib.md5()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def upload_files(sum):
    num_files = 5
    min_size_mb = 100
    max_size_mb = 500

    # 获取当前时间，并格式化为目录名
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    network_directory = r"\\192.168.4.230\共享文件夹\------------项目------------\傲梅恢复之星\测试数据"
    output_directory = os.path.join(network_directory, current_time+f"第 {sum} 次增量")
    os.makedirs(output_directory, exist_ok=True)  # 创建目录（如果不存在）

    filenames = []
    md5_set = set()

    while len(filenames) < num_files:
        size_mb = random.randint(min_size_mb, max_size_mb)
        filepath = os.path.join(output_directory, f"file_{len(filenames) + 1}.bin")

        # 生成文件并检查其MD5
        generate_unique_file(filepath, size_mb)
        file_md5 = get_md5(filepath)

        if file_md5 not in md5_set:
            md5_set.add(file_md5)
            filenames.append(filepath)
        else:
            # 如果MD5值重复，删除文件并重新生成
            os.remove(filepath)

    print("生成的文件及其MD5:")
    for filepath in filenames:
        print(f"{filepath}: {get_md5(filepath)}")


