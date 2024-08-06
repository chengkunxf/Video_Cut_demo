import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import time

def preprocess_text(text):
    """
    对输入文本进行预处理，包括去除文件后缀名、"_chunk_序号" 部分、
    标点符号和特殊字符，并进行中文分词。

    参数:
    text (str): 输入的待处理文本。

    返回:
    str: 预处理和分词后的文本。
    """
    # 去除文件后缀名
    text = re.sub(r'\.\w+', '', text)
    # 去除_chunk_序号
    text = re.sub(r'_chunk_\d+', '', text)
    # 去除标点符号和特殊字符，只保留字母、数字和中文
    text = re.sub(r'[^\w\s]', '', text)
    # 使用jieba进行分词
    words = jieba.lcut(text)
    return ' '.join(words)

def is_similar(text1, text2, threshold=0.7):
    """
    计算两个文本的相似度，并与阈值比较后返回布尔值。

    参数:
    text1 (str): 第一个输入文本。
    text2 (str): 第二个输入文本。
    threshold (float): 相似度阈值，默认值为0.65。

    返回:
    bool: 如果相似度大于阈值则返回 True，否则返回 False。
    float: 匹配用时（秒）。
    """
    start_time = time.time()
    
    # 文本预处理和分词
    text1_processed = preprocess_text(text1)
    text2_processed = preprocess_text(text2)

    # 向量化
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([text1_processed, text2_processed])

    # 计算余弦相似度
    cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    
    end_time = time.time()
    duration = end_time - start_time

    # 返回匹配结果和匹配用时
    return cosine_sim[0][0] > threshold, duration

# 测试函数（可选）
if __name__ == "__main__":
    text1 = "李白｜大唐反贼？一个视频，看懂李白被嫌弃的一生.mp4"
    text2 = "一口气看完李白一生大唐有你才真的了不起"
    result, duration = is_similar(text1, text2)
    print("匹配结果:", result)
    print("匹配用时: {:.4f} 秒".format(duration))
