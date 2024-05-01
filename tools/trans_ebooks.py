import os
import chardet
import codecs

def detect_file_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
        return result['encoding']

def split_file(file_path, output_dir, max_chars=100000):
    file_name = os.path.basename(file_path)
    base_name, _ = os.path.splitext(file_name)
    output_folder = os.path.join(output_dir, f"transform_{base_name}")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    encoding = detect_file_encoding(file_path)
    file_number = 1
    with codecs.open(file_path, 'r', encoding=encoding) as f:
        total_chars = 0
        while True:
            output_file_path = os.path.join(output_folder, f"{base_name}_{file_number}.txt")
            with codecs.open(output_file_path, 'w', encoding='UTF-16 LE') as out_f:
                for _ in range(max_chars):
                    char = f.read(1)
                    if not char:
                        break
                    out_f.write(char)
                    total_chars += 1
                    if total_chars % 10000 == 0:  # Update progress every 10,000 characters
                        print(f"Processing {file_name}: {total_chars} characters processed...")
                else:
                    # Read max_chars chars, continue to next file
                    file_number += 1
                    continue
                break  # Break the loop if file ends

def process_directory(directory_path):
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                split_file(file_path, root)

if __name__ == '__main__':
    directory_path = input("请输入包含txt文件的文件夹路径: ")
    process_directory(directory_path)
