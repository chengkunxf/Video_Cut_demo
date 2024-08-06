# main.py

import subprocess
import time
import os

def main():
    scripts = [
        "del_file.py",
        "requests_srt.py",
        "srt_ex.py",
        "token_cut.py",
        "video_ans_1.py",
        "video_cut.py"
    ]

    # 动态获取 .venv\Scripts\python.exe 的路径
    venv_path = os.path.join(os.getcwd(), '.venv', 'Scripts', 'python.exe')

    # 检查虚拟环境路径是否存在
    if not os.path.exists(venv_path):
        print(f"虚拟环境路径 {venv_path} 不存在，请检查路径是否正确。")
        return

    for script in scripts:
        print(f"正在运行 {script}...")
        try:
            result = subprocess.run([venv_path, script], env=os.environ)
            if result.returncode != 0:
                print(f"{script} 运行失败，返回码 {result.returncode}。")
                break
        except Exception as e:
            print(f"运行 {script} 时出错：{e}")
            break
        print(f"完成 {script}，等待 2 秒后运行下一个脚本。")
        time.sleep(2)

if __name__ == "__main__":
    main()
