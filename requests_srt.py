import requests
import yaml
import json
import logging
import os

# 设置日志配置
logging.basicConfig(filename='api_requests.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8')

def extract_video_url(file_path):
    """从指定的 YAML 文件中提取视频信息并返回 URL 列表."""
    with open(file_path, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)

    urls = []
    for video in data['videos']:
        urls.append(video['url'])
    
    return urls

def sanitize_filename(filename):
    """移除文件名中的非法字符."""
    return "".join(char for char in filename if char.isalnum() or char in (' ', '.', '_')).rstrip()

def save_json_response(response, title):
    """将 JSON 响应保存到以标题命名的文件中."""
    sanitized_title = sanitize_filename(title)
    directory = r'Data\Srt_Json\\'
    if not os.path.exists(directory):
        os.makedirs(directory)
        
    file_name = os.path.join(directory, f'{sanitized_title}.json')
    print(file_name)
    with open(file_name, 'w', encoding='utf-8') as json_file:
        json.dump(response, json_file, ensure_ascii=False, indent=4)

def main(yaml_file):
    urls = extract_video_url(yaml_file)
    api_url = "https://bibigpt.co/api/open/*****"#bibigpt 字幕请求API

    for video_url in urls:
        data = {
            "url": video_url,
            "includeDetail": 'false'
        }

        try:
            response = requests.post(api_url, json=data)
            response.raise_for_status()  # 如果请求失败，抛出异常

            response_json = response.json()
            title = response_json.get('detail', {}).get('title', 'no_title')  # 从detail字段中提取标题，默认值为'no_title'
            
            # 去除 "横板视频" 和 "竖版视频"
            title = title.replace("横板视频", "").replace("竖版视频", "")

            # 如果包含 '-' 且在 '-' 之前有内容，则去除 '-' 及其之前的内容
            if '-' in title:
                index = title.find('-')
                if index > 0:
                    title = title[index + 1:].strip()

            save_json_response(response_json, title)
            logging.info(f'成功保存 {video_url} 的响应数据，文件名: {title}.json。')
            print(f'成功保存 {video_url} 的响应数据，文件名: {title}.json。')

        except requests.exceptions.RequestException as e:
            logging.error(f'请求失败，视频 URL: {video_url}，错误: {e}')
            print(f'请求失败，视频 URL: {video_url}，错误: {e}')

if __name__ == "__main__":
    main('video_url.yaml')  # 替换为你的实际 YAML 文件路径
