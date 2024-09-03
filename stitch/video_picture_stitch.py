import cv2
import random
import glob
import numpy as np
import copy
import os

def extract_frames_from_video(video_path, step=30):
    cap = cv2.VideoCapture(video_path)
    frames = []
    count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if count % step == 0:
            frames.append(frame)
        count += 1
    cap.release()
    return frames


def save_frames_from_video(video_path, save_dir, step=10, ww=[0, 1], wh=[0, 1], direction='P'):
    frames = extract_frames_from_video(video_path, step)
    N=len(frames)
    h = frames[0].shape[0]
    w = frames[0].shape[1]
    c = 0
    for n, frame in enumerate(frames):
        image = frame[int(wh[0]*h):int(wh[1]*h), int(ww[0]*w):int(ww[1]*w), :]
        if n==0:
            pre_image = image*0
        if np.mean(np.abs(pre_image-image))>10:
            c+=1
            if direction == 'P': #正向行驶
                cv2.imwrite(save_dir + "/{}.png".format(str((n+1)).zfill(4)), image)
            elif direction == 'N':#逆向行驶
                cv2.imwrite(save_dir + "/{}.png".format(str((N-n)).zfill(4)), image)
            else:
                print("Direction Parameter should be 'N' or 'P'!")
                exit(-1)
        pre_image = copy.deepcopy(image)
    return frames



def MSE(img1, img2):
    mse = np.mean((img1 - img2) ** 2)
    return mse



def stitch_horizontal_images(images_path, output_path, src_points=None, dst_points=None):
    img_left = cv2.imread(images_path[0], 1)
    if src_points is not None:
        gray_left = cv2.cvtColor(img_left, cv2.COLOR_BGR2GRAY)
        gray_left, M = correct_perspective(gray_left, src_points, dst_points)
        img_left = cv2.warpPerspective(img_left, M, (img_left.shape[1], img_left.shape[0]))
    for n in range(1, len(images_path)):
        img_right = cv2.imread(images_path[n])
        if src_points is not None:
            img_right = cv2.warpPerspective(img_right, M, (img_right.shape[1], img_right.shape[0]))
        hxxs = []
        for v in range(4, img_right.shape[1]):
            im1 = np.array(cv2.cvtColor(img_left[:, -v:, :], cv2.COLOR_BGR2GRAY), dtype='float32')
            im2 = np.array(cv2.cvtColor(img_right[:, :v, :], cv2.COLOR_BGR2GRAY), dtype='float32')
            r = MSE(im1, im2)
            hxxs.append(r)
        index = np.where(hxxs == np.min(hxxs))
        index = index[0][0] if len(index[0]) > 0 else 0
        img_left = np.concatenate([img_left, img_right[:, index:, :]], 1)  # 从左往右拼接
    cv2.imwrite(output_path, img_left)


def correct_perspective(image, src_points, dst_points):
    # 读取图像
    height, width = image.shape[:2]
    # 计算透视变换矩阵
    M = cv2.getPerspectiveTransform(np.float32(src_points), np.float32(dst_points))
    # 进行透视变换
    corrected_image = cv2.warpPerspective(image, M, (width, height))
    return corrected_image, M


def stitch_up_images(images_path, output_path, src_points=None, dst_points=None):
    img_up = cv2.imread(images_path[0], 1)
    if src_points is not None:
        gray_up = cv2.cvtColor(img_up, cv2.COLOR_BGR2GRAY)
        gray_up, M = correct_perspective(gray_up, src_points, dst_points)
        img_up = cv2.warpPerspective(img_up, M, (img_up.shape[1], img_up.shape[0]))
    for n in range(1, len(images_path)):
        img_down = cv2.imread(images_path[n])
        if src_points is not None:
            img_down = cv2.warpPerspective(img_down, M, (img_down.shape[1], img_down.shape[0]))
        mses = []
        for v in range(4, img_down.shape[0]):
            im1 = np.array(cv2.cvtColor(img_up[-v:, :, :], cv2.COLOR_BGR2GRAY), dtype='float32')
            im2 = np.array(cv2.cvtColor(img_down[:v, :, :], cv2.COLOR_BGR2GRAY), dtype='float32')
            r = MSE(im1, im2)
            mses.append(r)
        index = np.where(mses == np.min(mses))
        index = index[0][0] if len(index[0]) > 0 else 0
        img_up = np.concatenate([img_up, img_down[index:, :, :]], 0)
    cv2.imwrite(output_path, img_up)


if __name__ == '__main__':
    random.seed(2024)
    step = 20 #帧率
    ww = [0.4, 0.6]#[0, 1]#横向窗口比例区间
    wh = [0, 1]#纵向窗口比例区间
    direction = 'N'#车行驶方向，从右至左，从后往前，反之为N
    extraction = True #是否需要提取图像
    file = r"data\video708\CD2R\2024-07-08-11-33-46.mp4"
    save_path = file.replace('.mp4', '')
    if not os.path.exists(save_path):
        os.makedirs(save_path, exist_ok=True)
    if extraction:
        save_frames_from_video(file, save_path, step=step, ww=ww, wh=wh, direction=direction)
    ##如找不到无畸变的视窗，可以基于提取的图像进行畸变矫正
    affine = False #是否使用仿射变换
    height = 288 #窗口图高度
    up_p = [203, 977]#图片最上方车子顶角横坐标
    down_p = [181, 1053]#图片最下方车子顶角横坐标
    src_points = [[up_p[0], 0], [up_p[1], 0], [down_p[0], height], [down_p[1], height]]
    dst_points = [[down_p[0], 0], [down_p[1], 0], [down_p[0], height], [down_p[1], height]]
    images = glob.glob(save_path + '/*.png')
    savepath = save_path + '/fullview.bmp'
    if affine:
        if '2U' in file or '3U' in file:
            stitch_up_images(images, savepath, src_points, dst_points)
        else:
            stitch_horizontal_images(images, savepath, src_points, dst_points)
    else:
        if '2U' in file or '3U' in file:
            stitch_up_images(images, savepath)
        else:
            stitch_horizontal_images(images, savepath)
