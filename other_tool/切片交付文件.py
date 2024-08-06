import os

# 设置网络路径
network_path = r'\\192.168.2.82\交付'
output_file = os.path.join(network_path, '视频切片结构.md')

# 初始化Markdown内容
markdown_content = "# 视频切片结构\n\n"

try:
    for root, dirs, files in os.walk(network_path):
        # 处理一级标题（文件夹名）
        if root != network_path:  # 忽略根目录
            folder_name = os.path.basename(root)
            markdown_content += f"## {folder_name}\n"
            
            # 处理文件
            for file in files:
                file_name, file_ext = os.path.splitext(file)  # 分离文件名和扩展名
                file_path = os.path.join(root, file)
                # 转换文件路径为相对路径
                relative_file_path = os.path.relpath(file_path, network_path)
                # 替换反斜杠为正斜杠以便于Markdown文件链接使用
                relative_file_path = relative_file_path.replace('\\', '/')
                markdown_content += f"## {file_name}\n"
                markdown_content += "- 简介：\n"
                markdown_content += f"- 视频链接：[{file}]({file_path})\n"
                markdown_content += "\n"  # 添加空行以分隔不同文件

    # 创建并写入Markdown文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(markdown_content)

    print(f"Markdown 文件已创建: {output_file}")

except Exception as e:
    print(f"访问失败: {e}")
