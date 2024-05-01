import os,codecs

def list_txt_files(directory):
    # 获取目录下的所有文件
    files = os.listdir(directory)
    # 筛选出所有的txt文件
    txt_files = [f for f in files if f.endswith('.txt')]
    # 将文件名用逗号连接起来
    return ','.join(txt_files)

def save_to_file(output_path, content, encoding='UTF-16 LE'):
    # 将内容以指定编码写入到文件
    with codecs.open(output_path, 'w', encoding=encoding) as f:
        f.write(content)

if __name__ == '__main__':
    while True:
        directory_path = input("请输入包含txt文件的文件夹路径: ")
    # 检查目录是否存在
        if not os.path.isdir(directory_path):
            print("提供的路径不是有效的目录。")
            break
        else:
        # 获取txt文件列表
            txt_files = list_txt_files(directory_path)
        # 构建输出文件路径
            output_file_path = os.path.join(directory_path, 'pages.txt')
        # 将txt文件列表保存到pages.txt，使用UTF-16 LE编码
            save_to_file(output_file_path, txt_files)
            print(f"输出已保存到 {output_file_path}")
