import os
import zipfile
import random
import subprocess

# 检查目录是否包含11个txt文件，其中至少有一个是pages.txt
def check_directory(directory):
    files = os.listdir(directory)
    txt_files = [f for f in files if f.endswith('.txt')]
    if len(txt_files) == 11 and 'pages.txt' in txt_files:
        return True
    else:
        return False

def copy_bin_file(bin_file_path, target_path):
    subprocess.run(['copy', bin_file_path, target_path], check=True)

def move_txt_to_zip(zip_path, directory):
    with zipfile.ZipFile(zip_path, 'a') as zipf:
        for filename in os.listdir(directory):
            if filename.endswith('.txt'):
                zipf.write(os.path.join(directory, filename), arcname=os.path.join('assets', filename))
                os.remove(os.path.join(directory, filename))

def edit_app_json(zip_path):
    random_number = str(random.randint(1000000, 9999999))
    with zipfile.ZipFile(zip_path, 'r') as zipf:
        with zipf.open('app.json', 'r') as f:
            app_json_content = f.read().decode('utf-8')
            app_json_content = app_json_content.replace('23300', random_number)
    
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        zipf.writestr('app.json', app_json_content)


def main():
    directory = input("请输入包含子文件夹的目录路径: ")
    bin_file_path = input("请输入bin文件的路径: ")

    # 检查所有子目录
    subdirectories = [os.path.join(directory, d) for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]
    for subdir in subdirectories:
        if not check_directory(subdir):
            print(f"目录 {subdir} 不满足条件，终止执行。")
            return

    # 处理每个子目录
    for subdir in subdirectories:
        # 创建bin文件的副本
        bin_copy_path = os.path.join(subdir, 'copy_of_bin_file.bin')
        copy_bin_file(bin_file_path, bin_copy_path)

        # 将txt文件移动到zip文件的assets目录下
        move_txt_to_zip(bin_copy_path, subdir)

        # 编辑zip文件内的app.json
        edit_app_json(bin_copy_path)

    print("所有操作已完成。")

if __name__ == "__main__":
    main()
