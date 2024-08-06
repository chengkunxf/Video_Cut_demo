import os
import re
import yaml
import json
import logging
import sys
from openai import OpenAI

# 配置日志功能，确保日志输出为中文且不会乱码
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[
    logging.FileHandler("app.log", encoding='utf-8'),
    logging.StreamHandler(sys.stdout)
])

def load_config(config_path='config.yaml'):
    try:
        logging.info(f"正在加载配置文件：{config_path}")
        with open(config_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
        logging.info("配置文件加载成功")
        return config
    except FileNotFoundError:
        logging.error("配置文件未找到")
        return None
    except yaml.YAMLError as e:
        logging.error(f"解析YAML文件出错：{e}")
        return None

# 定义一个函数，用OpenAI GPT总结字幕内容
def summarize_subtitles(subtitles, api_key, base_url,model):
    try:
        logging.info("正在使用OpenAI GPT总结字幕内容")
        client = OpenAI(api_key=api_key, base_url=base_url)
        all_text = ' '.join(subtitles)
        logging.debug(f"合并后的字幕文本：{all_text[:50]}...")
        completion = client.chat.completions.create(
            model= model,
            messages=[
                {"role": "system", "content": """按照字幕的行文内容与时间顺序，归纳讲述了那些事（20字以内），content，提取成标题，title,start_time 与 end_time 时间点，只以json格式返回， 输出格式{ "content"：“×××”,"title": "×××", "start_time": "00:06:02,769", "end_time": "00:06:23,420"} ，要求归纳的每件事不能过短，时长不低于30秒，并严格按照行文与时间顺序，时间一定要衔接上，不能出现时间衔接缺失，不能出现开头与结尾的内容的缺失。"""},
                {"role": "user", "content": str(all_text)}
            ]
        )
        
        if completion and completion.choices and len(completion.choices) > 0:
            summary = completion.choices[0].message.content.strip()
            logging.debug(f"API响应内容：{summary}")
            summary_points = summary.split('\n')
            logging.info("字幕总结成功")
            print(summary_points)
            return summary_points
        else:
            logging.error("API响应格式异常")
            return None
    except Exception as e:
        logging.error(f"OpenAI API调用出错：{e}")
        return None

def extract_and_reformat_json(input_data):
    logging.info("正在提取和重新格式化JSON数据")
    if isinstance(input_data, list):
        text = " ".join(input_data)
    else:
        text = input_data

    if '```json' in text and '```' in text:
        text = text.replace('```json', '').replace('```', '').strip()

    json_pattern = re.compile(r'\{.*?\}', re.DOTALL)
    json_matches = json_pattern.findall(text)

    reformatted_json_list = []
    for match in json_matches:
        try:
            json_data = json.loads(match)
            reformatted_json = {
                'start_time': json_data.get('start_time', '00:00:00,000'),
                'end_time': json_data.get('end_time', '00:00:00,000'),
                'content': json_data.get('content', '内容缺失'),
                'title': json_data.get('title', '标题缺失')
            }
            reformatted_json_list.append(reformatted_json)
        except json.JSONDecodeError:
            logging.warning(f"无法解析JSON数据：{match}")
            continue

    logging.info("JSON数据提取和重新格式化成功")
    return reformatted_json_list

def save_json_to_file(data, filename):
    try:
        logging.info(f"正在将JSON数据保存到文件：{filename}")
        with open(filename, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)
        logging.info("JSON数据保存成功")
    except Exception as e:
        logging.error(f"保存JSON数据到文件出错：{e}")

def retry_summarization(subtitles, api_key,base_url,model):
    for attempt in range(2):  # 进行一次重试，所以总共尝试2次
        summary_points = summarize_subtitles(subtitles, api_key,base_url,model)
        if summary_points:
            reformatted_json = extract_and_reformat_json(summary_points)
            if reformatted_json:
                return reformatted_json
        logging.warning(f"总结字幕内容尝试 {attempt + 1} 次失败")
    return None

def load_srt_files_from_directory(base_path='Data/Srt_temp'):
    srt_data = {}
    for folder in os.listdir(base_path):
        folder_path = os.path.join(base_path, folder)
        if os.path.isdir(folder_path):
            srt_contents = []
            for file in os.listdir(folder_path):
                if file.endswith('.srt'):
                    file_path = os.path.join(folder_path, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            srt_content = f.readlines()
                        srt_contents.append((file, srt_content))
                    except Exception as e:
                        logging.error(f"Error reading file {file_path}: {e}")
            if srt_contents:
                srt_data[folder] = srt_contents
    return srt_data

def save_summarized_json(summarized_data, folder, file_name):
    output_folder = os.path.join('Data', 'Srt_cut_list', folder)
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, file_name.replace('.srt', '.json'))
    save_json_to_file(summarized_data, output_path)

if __name__ == "__main__":
    config = load_config()
    if not config:
        logging.critical("加载配置失败，程序退出")
        exit("加载配置失败")
    
    api_key = config.get('api_key')
    base_url = config.get('base_url')
    model = config.get('model')
    if not api_key:
        logging.critical("配置中未找到API密钥，程序退出")
        exit("配置中未找到API密钥")
    
    srt_data = load_srt_files_from_directory()
    
    if not srt_data:
        logging.critical("未找到任何SRT文件，程序退出")
        exit("未找到任何SRT文件")
    
    for folder, srt_files in srt_data.items():
        for file_name, srt_content in srt_files:
            summary_points = retry_summarization(srt_content, api_key,base_url,model)
            if summary_points:
                save_summarized_json(summary_points, folder, file_name)
                for point in summary_points:
                    print(f"开始时间: {point['start_time']}, 结束时间: {point['end_time']}, 摘要: {point['content']}, 标题: {point['title']}")
            else:
                logging.critical(f"总结字幕内容失败，文件夹：{folder}，文件：{file_name}")
                exit("总结字幕内容失败")
