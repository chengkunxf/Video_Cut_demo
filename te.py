def process_title(response_json):
    # 从 response_json 中提取 title，提供默认值 'no_title'
    title = response_json.get('detail', {}).get('title', 'no_title')
    
    # 去除 "横板视频" 和 "竖版视频"
    title = title.replace("横板视频", "").replace("竖版视频", "")
    
    # 如果包含 '-' 且在 '-' 之前有内容，则去除 '-' 及其之前的内容
    if '-' in title:
        index = title.find('-')
        if index > 0:
            title = title[index + 1:].strip()
    
    return title

# 测试用例
test_cases = [
    {"response_json": {"detail": {"title": "示例标题-横板视频-更多内容"}}, "expected": "更多内容"},
    {"response_json": {"detail": {"title": "竖版视频-示例标题"}}, "expected": "示例标题"},
    {"response_json": {"detail": {"title": "无特殊字符的标题"}}, "expected": "无特殊字符的标题"},
    {"response_json": {"detail": {"title": "无特殊字符的-标题"}}, "expected": "标题"},
    {"response_json": {"detail": {"title": "横板视频竖版视频示例标题"}}, "expected": "示例标题"},
    {"response_json": {"detail": {"title": "横板视频-竖版视频-示例标题"}}, "expected": "示例标题"},
    {"response_json": {"detail": {"title": "示例-横板视频-标题"}}, "expected": "标题"},
    {"response_json": {"detail": {}}, "expected": "no_title"},
    {"response_json": {}, "expected": "no_title"}
]

# 执行测试
for i, test_case in enumerate(test_cases):
    result = process_title(test_case["response_json"])
    assert result == test_case["expected"], f"Test case {i+1} failed: expected '{test_case['expected']}', but got '{result}'"
    print(f"Test case {i+1} passed: '{result}'")

print("All test cases passed.")
