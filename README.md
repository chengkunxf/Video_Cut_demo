# Ai视频切片demo

## 切片流程

### 先填入视频url链接

   1. 使用的是 <https://bibigpt.co/> 的api接口，好处是不用下载资源视频直接返回字幕json文件，B站、youtube等主流平台都可直接提取字幕
   2. 也可以使用其他语言转文字工具提取SRT文件，如本地使用fast_whisper等
   3. 在video_url.yaml文件中的url链接填入对应的视频链接


### 获取字幕json文件 requests_srt.py

   1. requests_srt.py 文件使用BIBIGPT的api接口，请求视频字幕，获取的字幕文件
   2. 存入Data\Srt_Json

### 提取srt字幕文件 srt_ex.py

   1. 接口返回的是一个包含视频title、字幕时间与内容的json文件，需要将其处理成类SRT格式以便后续的AI生成视频切片表
   2. 存入Data\Srt_ex

### 切分chunk块  token_cut.py

   1. 提取的SRT字幕文件，文本量太大无法直接发给AI生成视频切片表，因此需要啊做Chunk切分，每个Chunk的Token数大小限制在5000-7000
   2. 一般一个2w字符（包含时间戳）的字幕文件切分成3个Chunk块左右
   3. \存入Data\Srt_temp\视频名\chunk.srt文件

### AI进行视频分析。获取视频切片表 video_ans_1.py

   1. 这里使用的是openai的api，其他大模型效果没有测试如deepseek等，可能需要进行提示词调优
   2. 相关参数在config.yaml中配置
   3. 返回的视频切片josn表 存入Data\Srt_cut_list\视频名\chunk.json

### 根据视频切片表进行切片处理 video_cut.py

   1. 原视频放入Video文件夹，与获取的字幕文件同名，为了避免有个别字符不一致，使用余弦相似度进行匹配。cosin_march.py
   2. 存入Video\视频名\视频切片

## 程序流程

main.py入口运行

1. del_file.py （删除已生成的临时文件）
2. requests_srt.py
3. srt_ex.py
4. token_cut.py
5. video_ans_1.py  
6. video_cut.py
