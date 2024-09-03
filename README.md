# Code

用于车厢图像拼接

该项目提供了从视频中提取帧并将其拼接成完整车厢图像的工具，主要应用于车载视频的图像处理与拼接。

项目简介

本项目旨在从视频中提取指定帧，然后对这些帧进行横向或纵向拼接，最终得到一个完整的车厢图像。用户可以指定视频中需要提取的帧的步长，以及在拼接过程中是否进行畸变矫正。

功能说明
帧提取：从指定视频中按设定的步长提取帧。
图像拼接：支持横向和纵向拼接图像，提供了基本的仿射变换以处理视角问题。
畸变矫正：基于用户提供的源点和目标点进行透视变换，修正图像畸变。


环境依赖
在使用此代码前，请确保你的Python环境安装了以下依赖包：

OpenCV (cv2)
Numpy (numpy)
Glob (glob)


安装方式：

pip install opencv-python numpy


## 使用方法
1. 提取视频帧并保存
使用 save_frames_from_video 函数从视频中提取帧并保存。以下是使用示例：
```
video_path = "data/video708/CD2R/2024-07-08-11-33-46.mp4"
save_dir = "data/video708/CD2R/frames"
step = 20  # 每20帧提取一帧
ww = [0.4, 0.6]  # 横向窗口比例区间
wh = [0, 1]  # 纵向窗口比例区间
direction = 'N'  # 车行驶方向，从右至左

save_frames_from_video(video_path, save_dir, step=step, ww=ww, wh=wh, direction=direction)
```

2. 拼接图像
帧提取完成后，可以使用 stitch_horizontal_images 或 stitch_up_images 函数对图像进行拼接。以下是拼接图像的示例：

```
images = glob.glob("data/video708/CD2R/frames/*.png")
output_path = "data/video708/CD2R/fullview.bmp"

# 直接拼接
stitch_horizontal_images(images, output_path)

# 如果需要透视变换矫正
src_points = [[203, 0], [977, 0], [181, 288], [1053, 288]]
dst_points = [[181, 0], [1053, 0], [181, 288], [1053, 288]]
stitch_horizontal_images(images, output_path, src_points, dst_points)
```

## 注意事项
3. 注意事项
视频分辨率：请确保输入视频的分辨率适用于你指定的窗口比例 ww 和 wh。
仿射变换：在进行拼接时，如果出现图像畸变，可以使用提供的透视变换功能进行矫正。
性能优化：对于长时间的视频和高分辨率的图像，建议调整步长 step 以控制帧的提取频率。


项目结构

.
├── data/                     
│   └── video708/
│       └── CD2R/                 
│           ├── 2024-07-08-11-33-46test/  # 测试数据保存目录
│           ├── 2024-07-08-11-33-46.jpg   # 测试视频对应的帧图像
│           ├── 2024-07-08-11-33-46.mp4   # 测试视频文件
│           ├── 2024-07-08-11-34-12.jpg   
│           ├── 2024-07-08-11-34-12.mp4   
│           ├── 2024-07-08-11-38-46.jpg   
│           ├── 2024-07-08-11-38-46.mp4   
│           ├── ...                       # 省略其他视频及其对应的帧图像
├── video_picture_stitch.py       # 图像拼接的主要代码文件
└── README.md                     # 项目说明文件


贡献