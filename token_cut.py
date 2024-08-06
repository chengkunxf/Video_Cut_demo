import tiktoken
import re
import os

# 指定模型和文件夹路径
MODEL = "gpt-4o-2024-05-13"
SRT_INPUT_FOLDER = os.path.join('Data', 'Srt_ex')  # 输入文件夹路径
CHUNK_OUTPUT_FOLDER = os.path.join('Data', 'Srt_temp')  # 输出文件夹路径

# 定义最大和最小 token 数以及重叠字符数
MAX_TOKENS = 7000
MIN_TOKENS = 5000
OVERLAP_CHARS = 75

# 提取时间标记的正则表达式 (分秒格式)
TIMESTAMP_PATTERN = re.compile(r'^\d{2}:\d{2} --> \d{2}:\d{2} .*')

def init_encoding(model):
    """初始化编码器"""
    return tiktoken.encoding_for_model(model)

def validate_folder(path):
    """检查文件夹是否存在"""
    if not os.path.exists(path):
        os.makedirs(path)
        #raise FileNotFoundError(f"文件夹未找到: {path}")

def get_srt_files(path):
    """获取所有 .srt 文件"""
    return [f for f in os.listdir(path) if f.endswith('.srt')]

def is_valid_line(line):
    """检查行是否符合时间标记的要求"""
    return bool(TIMESTAMP_PATTERN.match(line.strip()))

def find_split_point(tokens, start, end):
    """找到合适的分割点"""
    while end > start and len(tokens[start:end]) > MAX_TOKENS:
        end -= 1
    return end

def clean_chunk(chunk_text):
    """检查并清理 chunk 中的时间结构"""
    lines = chunk_text.split('\n')
    cleaned_lines = [line for line in lines if is_valid_line(line)]
    return '\n'.join(cleaned_lines)

def process_srt_file(file_path, encoder):
    """处理单个 srt 文件"""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    encoded_tokens = encoder.encode(content)
    num_tokens = len(encoded_tokens)
    chunks = []

    i = 0
    while i < num_tokens:
        start = i
        end = min(i + MAX_TOKENS, num_tokens)
        split_point = find_split_point(encoded_tokens, start, end)

        if split_point - start < MIN_TOKENS:
            split_point = min(start + MAX_TOKENS, num_tokens)

        chunk_tokens = encoded_tokens[start:split_point]
        chunk_text = encoder.decode(chunk_tokens)

        if start > 0:
            overlap_start = encoder.decode(encoded_tokens[max(0, start - OVERLAP_CHARS):start])
            chunk_text = overlap_start + chunk_text

        if split_point < num_tokens:
            overlap_end = encoder.decode(encoded_tokens[split_point:min(split_point + OVERLAP_CHARS, num_tokens)])
            chunk_text += overlap_end

        cleaned_chunk_text = clean_chunk(chunk_text)

        if len(cleaned_chunk_text) >= 300:
            chunks.append(cleaned_chunk_text)
        i = split_point

    return chunks

def save_chunks(chunks, srt_file):
    """保存处理后的 chunks"""
    output_folder = os.path.join(CHUNK_OUTPUT_FOLDER, os.path.splitext(srt_file)[0])
    os.makedirs(output_folder, exist_ok=True)
    for idx, chunk in enumerate(chunks):
        chunk_file_path = os.path.join(output_folder, f"{os.path.splitext(srt_file)[0]}_chunk_{idx + 1}.srt")
        with open(chunk_file_path, 'w', encoding='utf-8') as chunk_file:
            chunk_file.write(chunk)
        print(f"Chunk {idx + 1} saved to {chunk_file_path}")

def main():
    """主函数"""
    enc = init_encoding(MODEL)
    validate_folder(SRT_INPUT_FOLDER)
    validate_folder(CHUNK_OUTPUT_FOLDER)
    srt_files = get_srt_files(SRT_INPUT_FOLDER)

    for srt_file in srt_files:
        file_path = os.path.join(SRT_INPUT_FOLDER, srt_file)
        chunks = process_srt_file(file_path, enc)
        save_chunks(chunks, srt_file)

if __name__ == "__main__":
    main()
