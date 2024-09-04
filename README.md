# stitch - 车厢图像拼接工具

## 项目概述

专门用于处理和拼接运煤车厢视频。本工具提供了从视频中提取帧并将其拼接成完整车厢图像的功能，主要应用于车载视频的图像处理与分析。

## 待优化
对于视频帧率，行车方向等设置，后续都可优化成自动化设置。

## 功能特性

- **帧提取**：按指定步长从视频中提取帧。
- **图像拼接**：支持横向和纵向图像拼接，包含基础仿射变换处理。
- **畸变矫正**：通过用户定义的源点和目标点进行透视变换，校正图像畸变。

## 环境要求

确保您的Python环境中安装了以下依赖包：

- OpenCV (cv2)
- NumPy
- glob (Python标准库)

安装主要依赖：

```bash
pip install opencv-python numpy
```

## 使用指南

### 1. 视频帧提取

使用`save_frames_from_video`函数提取视频帧：

```python
from video_picture_stitch import save_frames_from_video

video_path = "data/video708/CD2R/2024-07-08-11-33-46.mp4"
save_dir = "data/video708/CD2R/frames"
save_frames_from_video(video_path, save_dir, step=20, ww=[0.4, 0.6], wh=[0, 1], direction='N')
```

### 2. 图像拼接

使用`stitch_horizontal_images`函数拼接图像：

```python
from video_picture_stitch import stitch_horizontal_images
import glob

images = glob.glob("data/video708/CD2R/frames/*.png")
output_path = "data/video708/CD2R/fullview.bmp"

# 基本拼接
stitch_horizontal_images(images, output_path)

# 带透视矫正的拼接
src_points = [[203, 0], [977, 0], [181, 288], [1053, 288]]
dst_points = [[181, 0], [1053, 0], [181, 288], [1053, 288]]
stitch_horizontal_images(images, output_path, src_points, dst_points)
```

## 项目结构

```
stitch/
│
├── data/
│   └── video708/
│       └── CD2R/
│           ├── frames/                   # 存放提取的视频帧
│           ├── 2024-07-08-11-33-46.mp4   # 示例视频文件
│           └── ...
│
├── video_picture_stitch.py               # 主要功能实现代码
└── README.md                             # 本文档
```

## 注意事项

- 确保视频分辨率与设定的窗口比例（`ww`和`wh`）相匹配。
- 对于大型视频文件，可通过调整`step`参数来优化性能。
- 如遇图像畸变问题，可利用提供的透视变换功能进行校正。

## 贡献指南


## 许可证



## 联系方式



