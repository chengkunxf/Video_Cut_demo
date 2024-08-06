import tiktoken

# 指定模型
enc = tiktoken.encoding_for_model("gpt-4o-2024-05-13")

# 读取文件内容
file_path = r'Data\Srt_ex\url_response_1\url_response_1_chunk_1.srt'  # 替换为你的文件路径

with open(file_path, 'r', encoding='utf-8') as file:
    content = file.read()

# 编码并统计 token 数
encoded_tokens = enc.encode(content)
num_tokens = len(encoded_tokens)

print(f"文件中的 token 数: {num_tokens}")