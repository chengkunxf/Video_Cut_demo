import os
import json
import subprocess
from cosin_march import is_similar  # 确保is_similar函数可以被正确导入

def split_video(input_file, segments, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    skipped_due_to_time = []
    skipped_due_to_existence = []
    
    for segment in segments:
        start_time = segment['start_time']
        end_time = segment['end_time']
        
        # 检查并修正时间格式
        start_time = start_time.replace(',', '.')
        end_time = end_time.replace(',', '.')
        
        # 确保 end_time 大于 start_time
        if start_time >= end_time:
            skipped_due_to_time.append((segment, "start_time 不小于 end_time"))
            continue
        
        title = segment['title']
        output_file = os.path.join(output_dir, f"{title}.mp4")
        
        # 检查输出文件是否已存在
        if os.path.exists(output_file):
            skipped_due_to_existence.append((segment, "输出文件已存在"))
            continue
        
        command = [
            'ffmpeg',
            '-i', input_file,
            '-ss', start_time,
            '-to', end_time,
            '-c', 'copy',
            output_file
        ]
        
        subprocess.run(command, check=True)
        print(f"生成了 {output_file} (开始时间: {start_time}, 结束时间: {end_time})")
    
    return skipped_due_to_time, skipped_due_to_existence

def read_json_segments(json_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        segments = json.load(file)
    print(f"读取了 JSON 文件: {json_file}")
    return segments

def find_matching_json_folder(video_name, json_base_dir):
    print(f"正在匹配视频文件: {video_name}")
    for folder_name in os.listdir(json_base_dir):
        folder_path = os.path.join(json_base_dir, folder_name)
        if os.path.isdir(folder_path):
            is_similar_result, _ = is_similar(video_name, folder_name)
            if is_similar_result:
                print(f"匹配到 JSON 文件夹: {folder_name}")
                return folder_path
    print(f"未匹配到任何 JSON 文件夹: {video_name}")
    return None

def process_videos_in_directory(video_directory, json_base_dir):
    total_skipped_due_to_time = []
    total_skipped_due_to_existence = []
    
    for root, _, files in os.walk(video_directory):
        for file in files:
            if file.endswith(('.mp4', '.mov', '.avi', '.mkv')):
                video_name = os.path.splitext(file)[0]
                matching_folder = find_matching_json_folder(video_name, json_base_dir)
                
                if matching_folder:
                    json_files = [f for f in os.listdir(matching_folder) if f.endswith('.json')]
                    
                    if json_files:
                        for json_file in json_files:
                            json_file_path = os.path.join(matching_folder, json_file)
                            segments = read_json_segments(json_file_path)
                            input_file = os.path.join(root, file)
                            output_dir = os.path.join(root, video_name)
                            skipped_due_to_time, skipped_due_to_existence = split_video(input_file, segments, output_dir)
                            total_skipped_due_to_time.extend(skipped_due_to_time)
                            total_skipped_due_to_existence.extend(skipped_due_to_existence)
                    else:
                        print(f"JSON 文件夹 {matching_folder} 中没有找到任何 JSON 文件。")
                else:
                    print(f"跳过视频文件: {video_name}，因为未找到匹配的 JSON 文件夹")
    
    # 输出跳过的片段信息
    print(f"总共跳过了 {len(total_skipped_due_to_time)} 个视频片段，原因是 end_time 不得小于 start_time")
    for segment, reason in total_skipped_due_to_time:
        print(f"片段 {segment['title']} 被跳过，原因: {reason}")

    print(f"总共跳过了 {len(total_skipped_due_to_existence)} 个视频片段，原因是输出文件已存在")
    for segment, reason in total_skipped_due_to_existence:
        print(f"片段 {segment['title']} 被跳过，原因: {reason}")

# 定义 JSON 文件夹和视频文件夹路径
json_base_dir = r'Data\Srt_cut_list'
video_directory = r'Video'

# 处理视频目录中的所有视频
process_videos_in_directory(video_directory, json_base_dir)
