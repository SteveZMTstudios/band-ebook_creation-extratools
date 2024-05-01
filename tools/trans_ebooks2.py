import os
import chardet
import math

# 定义分割和转码文件的函数
def process_file(file_path, target_encoding='UTF-16 LE'):
    # 使用chardet检测文件编码
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
        encoding = result['encoding']
    
    # 读取文件并解码
    with open(file_path, 'r', encoding=encoding) as f:
        content = f.read()

    # 计算需要分割的文件数量
    char_count = len(content)
    max_chars = 100000  # 每个文件最大字符数
    num_files = math.ceil(char_count / max_chars)

    # 创建存储分割后文件的目录
    dir_name, file_name = os.path.splitext(file_path)
    file_base_name = os.path.basename(dir_name)
    new_dir = os.path.join(os.path.dirname(dir_name), f'transform_{file_base_name}')
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)

    # 分割和转码文件
    for i in range(num_files):
        start = i * max_chars
        end = min((i + 1) * max_chars, char_count)
        # 确保不会切割半个汉字
        if end < char_count and content[end - 1].isalpha():
            end = content.rfind(' ', start, end) or end
        new_content = content[start:end]

        # 创建新文件名
        new_file_name = f'{file_base_name}_{i + 1:02d}{file_name}'
        new_file_path = os.path.join(new_dir, new_file_name)

        # 将内容编码并写入新文件
        with open(new_file_path, 'w', encoding=target_encoding) as f:
            f.write(new_content)
        
        print(f'File {new_file_name} has been processed and saved.')

# 定义处理目录下所有txt文件的函数
def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                process_file(file_path)

# 使用示例
directory_path = input("请输入包含txt文件的目录路径: ")
process_directory(directory_path)
