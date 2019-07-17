import os
import shutil

from PIL import Image


def compress(path_src: str) -> None:
    # 输入的路径。
    path_dst = '%s%s' % (path_src, '_resize')
    # 如果有存在目录就删除
    if os.path.exists(path_dst):
        shutil.rmtree(path_dst)
    # 新建目录
    os.mkdir(path_dst)
    file_list = os.listdir(path_src)
    for file in file_list:
        if is_picture(file):
            # 原图完整地址
            file_src = path_src + os.sep + file
            # 新图完整地址
            file_dst = path_dst + os.sep + file
            try:
                print('converting: ', file)
                src_img = Image.open(file_src)
                # 调用不同的压缩方法
                new_image = fit_to_fhd(src_img, src_img.size)
                new_image.save(file_dst)
            except IOError:
                print('convert fail: ', file)
            else:
                print(file, ': ', src_img.size, ' -> ', new_image.size)


# 直接压缩到 1920*1080，可能会失去原图比例，但是保留所有原图图像，这个相当于windows壁纸的“拉伸”
def resize_to_fhd(src_img: Image) -> Image:
    return src_img.resize((1920, 1080), Image.ANTIALIAS)


# fit 到 1920*1080，可能会失去部分原图图像，但是会保留原图比例，这个相当于windows壁纸的“填充”
def fit_to_fhd(src_img: Image, src_size: tuple = None) -> Image:
    width_old = src_size[0]
    height_old = src_size[1]

    # # 采用了先缩放到长和宽都不小于HD尺寸，并且保持比例
    if width_old / height_old / (16 / 9) > 1:
        width_new = int(width_old / height_old * 1080)
        height_new = 1080
    else:
        width_new = 1920
        height_new = int(height_old / width_old * 1920)
    # print(id(src_img)) 每次操作图像，都会返回一个新的对象，原来的对象不会改变
    temp_image = src_img.resize((width_new, height_new), Image.ANTIALIAS)
    # 裁剪一下，只有2种情况的需要裁剪，分别是胖的和瘦的。。
    if width_new == 1920 and height_new > 1080:
        # 注意，这里的4个值是构成的2个点的绝对坐标，分别是左上角的点和右下角的点。
        first_point_to_top = int((height_new - 1080) / 2)
        temp_image = temp_image.crop((0, first_point_to_top, 1920, height_new - first_point_to_top))
    elif height_new == 1080 and width_new > 1920:
        first_point_to_left = int((width_new - 1920) / 2)
        temp_image = temp_image.crop((first_point_to_left, 0, width_new - first_point_to_left, 1080))
    # 这里是防止出现 1081 这种上面除以2的时候产生的异常值。
    return temp_image.resize((1920, 1080), Image.ANTIALIAS)


def is_picture(file_name: str) -> bool:
    file_type = os.path.splitext(file_name)[1]
    if file_type.lower() in ('.jpg', '.png', '.jpeg'):
        return True
    else:
        return False


if __name__ == '__main__':
    compress(r'D:\1')
