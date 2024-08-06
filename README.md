# Ai_Video_Cut
Ai视频切片
## 切片流程：
1. 先填入视频url链接 video_url.yaml
2. 获取字幕json文件 requests_srt.py 存入Data\Srt_Json
3. 从json文件中提取srt字幕文件，srt_ex.py 存入Data\Srt_ex
4. 再切分chunk块  token_cut.py 存入Data\Srt_temp\视频名\chunk.srt文件
5. 发送给AI进行视频分析。获取视频切片表（json文件） video_ans _1.py  存入Data\Srt_cut_list\视频名\chunk.json
6. 根据视频切片表进行切片处理 video_cut.py 存入Video\视频名\视频切片




## 程序流程：
1. requests_srt.py 
2. srt_ex.py 
3. token_cut.py 
4. video_ans _1.py  
5. video_cut.py 