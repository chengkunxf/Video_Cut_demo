import json
import os

# 设置网络共享文件夹路径
md_file_path = r'\\192.168.2.82\交付\视频切片结构.md'
json_file_path = 'path_to_your_json_file.json'  # 替换为你的JSON文件路径

# 读取JSON文件并提取content值
with open(json_file_path, 'r', encoding='utf-8') as json_file:
    json_data = json.load(json_file)

# 读取Markdown文件
with open(md_file_path, 'r', encoding='utf-8') as md_file:
    md_content = md_file.readlines()

# 遍历JSON数据，找到匹配的标题并替换简介
for item in json_data:
    if 'title' in item and 'content' in item:
        title = item['title']
        content = item['content']
        found_title = False

        new_md_content = []
        for line in md_content:
            # 查找三级标题
            if line.strip() == f'## {title}':
                found_title = True
            # 在找到匹配标题后，查找并替换简介部分
            if found_title and line.startswith('- 简介：'):
                new_md_content.append(f'- 简介：{content}\n')
                found_title = False  # 重置为False以避免修改其他简介
            else:
                new_md_content.append(line)

        # 更新Markdown内容
        md_content = new_md_content

# 将修改后的内容写回Markdown文件
with open(md_file_path, 'w', encoding='utf-8') as md_file:
    md_file.writelines(md_content)

print("Markdown文件已更新")
