import os
import shutil

def delete_files_and_folders(base_path):
    has_files = False
    for root, dirs, files in os.walk(base_path):
        for name in files:
            has_files = True
            file_path = os.path.join(root, name)
            if base_path == 'Data/Srt_Json' and file_path.endswith('.json'):
                confirm = input(f"\033[91m警告！！！是否要删除 JSON 文件下的 {file_path}？(y/n): \033[0m")
                if confirm.lower() == 'y':
                    os.remove(file_path)
                    print(f"已删除 JSON 文件: {file_path}")
            else:
                os.remove(file_path)
                print(f"已删除文件: {file_path}")

        for name in dirs:
            has_files = True
            dir_path = os.path.join(root, name)
            shutil.rmtree(dir_path)
            print(f"已删除文件夹及其内容: {dir_path}")

    if not has_files:
        print(f"文件夹 {base_path} 下无文件。")

# 要清理的目录
directories_to_clean = ['Data/Srt_cut_list', 'Data/Srt_ex', 'Data/Srt_Json', 'Data/Srt_temp']

for directory in directories_to_clean:
    if os.path.exists(directory):
        delete_files_and_folders(directory)
    else:
        print(f"目录 {directory} 不存在。")
