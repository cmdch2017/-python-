# -python-
代码是根据需求的调整变化的，不一定最新代码就是符合你的，请注意！！！
本程序还自带提高分辨率1920:1080，以及增加10db声音的功能
### 最新：
批量视频分段.exe 根据规则将视频截取后合并，还能手动删掉片头和片尾曲，帮助你分段截取视频,代码videoSeperByFixedTimeTotalAddStartAndEnd.py
过往的版本：
videoSeperByFixedTimeTotal.py 增加了批量选择视频功能
videoSeperByFixedTime.py 是调整了需求，每隔300秒截取30秒视频，将截取的再拼成一个视频
### 最初的版本：
视频分段好助手.exe 手动输入截取视频的时间，分割每隔视频的分段，代码videoSeper.py


# 最新版本的使用说明：批量视频分段助手工具

欢迎使用批量视频分段助手工具！本工具旨在帮助您将视频文件按照指定的规则分割并合并，以生成您所需的视频。

## 步骤1：选择视频文件

1. 点击 "Select Multiple Input Files" 按钮，选择您要处理的视频文件。您可以同时选择多个视频文件。
2. 选择的文件将会显示在下方的文件列表中。

## 步骤2：设置分割和合并规则

1. 在 "Segment Interval (seconds):" 文本框中，输入希望分割视频的时间间隔（以秒为单位）。例如，若要每隔5分钟分割一次，输入300。
2. 在 "Segment Duration (seconds):" 文本框中，输入每个分割片段的持续时间（以秒为单位）。例如，若希望每个片段为30秒，输入30。
3. 在 "Start Time (seconds):" 文本框中，输入每个分割片段的起始时间（以秒为单位）。
4. 在 "End Time (seconds):" 文本框中，输入每个分割片段的结束时间（以秒为单位）。

## 步骤3：生成视频

1. 点击 "Generate Selected Videos" 按钮，工具将会按照您的设置生成分割后的视频。
2. 在生成的过程中，工具将在状态栏中显示当前进度。

## 步骤4：保存生成的视频

1. 生成完成后，工具将在指定的输出文件夹中保存生成的视频文件。
2. 输出文件的命名规则为 "merged_output.mp4"，若有重名文件，将会自动添加编号。

## 注意事项

- 本工具依赖于 FFmpeg 库进行视频处理，请确保您的电脑已安装 FFmpeg。
- 请确保您选择的视频文件格式为 MP4 格式。

## 联系我们

如有任何问题或建议，请随时联系我们：congminglst@163.cm
当然也许你想看一下博客https://blog.csdn.net/weixin_43914278/article/details/132489511?spm=1001.2014.3001.5502
