import os
import json

def json_to_srt(json_file, srt_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    with open(srt_file, 'w', encoding='utf-8') as file:
        for entry in data['detail']['subtitlesArray']:
            start_time = entry['startTime']
            end_time = entry['end']
            text = entry['text']

            # Convert time from seconds to MM:SS format
            start_time_srt = convert_time(start_time)
            end_time_srt = convert_time(end_time)

            file.write(f"{start_time_srt} --> {end_time_srt} {text}\n")

def convert_time(seconds):
    total_seconds = int(seconds)
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return f"{minutes:02}:{seconds:02}"

def process_folder(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith('.json'):
            json_file = os.path.join(input_folder, filename)
            srt_file = os.path.join(output_folder, filename.replace('.json', '.srt'))
            json_to_srt(json_file, srt_file)
            print(f"Converted {json_file} to {srt_file}")

# 设置输入和输出文件夹路径
input_folder = 'Data\Srt_Json'
output_folder = 'Data\Srt_ex'
process_folder(input_folder, output_folder)
