# !/usr/bin/python
# -*- coding: utf-8 -*-

import os
import subprocess
import time

# 1) Rotate 90 clockwise:
# https://stackoverflow.com/questions/3937387/rotating-videos-with-ffmpeg
#
# ffmpeg -i in.mov -vf "transpose=1" out.mov
# For the transpose parameter you can pass:
#
# 0 = 90CounterClockwise and Vertical Flip (default)
# 1 = 90Clockwise
# 2 = 90CounterClockwise
# 3 = 90Clockwise and Vertical Flip
# Use -vf "transpose=2,transpose=2" for 180 degrees.

# 2) Cut by time
# ffmpeg -i input.mp4 -ss 00:00:00 -to 00:00:05 -c copy output.mp4

# 3) Video adjustment
# contrast
# Set the contrast expression. The value must be a float value in range -2.0 to 2.0. The default value is "1".
#
# brightness
# Set the brightness expression. The value must be a float value in range -1.0 to 1.0. The default value is "0".
#
# saturation
# Set the saturation expression. The value must be a float in range 0.0 to 3.0. The default value is "1".
#
# gamma
# Set the gamma expression. The value must be a float in range 0.1 to 10.0. The default value is "1".
#
# gamma_r
# Set the gamma expression for red. The value must be a float in range 0.1 to 10.0. The default value is "1".
#
# gamma_g
# Set the gamma expression for green. The value must be a float in range 0.1 to 10.0. The default value is "1".
#
# gamma_b
# Set the gamma expression for blue. The value must be a float in range 0.1 to 10.0. The default value is "1".
#
# gamma_weight
# Set the gamma weight expression. It can be used to reduce the effect of a high gamma value on bright image areas,
# e.g. keep them from getting overamplified and just plain white. The value must be a float in range 0.0 to 1.0.
# A value of 0.0 turns the gamma correction all the way down while 1.0 leaves it at its full strength. Default is "1".

# Merge audio and video
# https://superuser.com/questions/801547/ffmpeg-add-audio-but-keep-video-length-the-same-not-shortest
# If video length is shorter than audio length, -shortest is what you want.
# If video length is longer than audio length, no flag at all will be what you want.

# https://video.stackexchange.com/questions/12905/repeat-loop-input-video-with-ffmpeg/12906
# Concat demuxer
# This allows you to loop an input without needing to re-encode.
#
# Make a text file. Contents of an example text file to repeat 4 times.
#
# file 'input.mp4'
# file 'input.mp4'
# file 'input.mp4'
# file 'input.mp4'
# Then run ffmpeg:
#
# ffmpeg -f concat -i list.txt -c copy output.mp4
# ffmpeg -f concat -safe 0 -i 1.txt -c copy a.mp3

# loop filter
# Example using the loop filter to loop 4 times, each loop is 75 frames,
# each loop skips the first 25 frames of the input:
#
# ffmpeg -i input -filter_complex loop=loop=3:size=75:start=25 output
# Or use the shorthand: loop=3:75:25
# Filtering requires re-encoding.
# This filter places all frames into memory.
# Using loop=3 will loop 4 times.
# To loop infinitely use -1.
# You must list the number of frames to loop (shown as 75 in the example above). Max value is 32767.
# Also see ffmpeg -h filter=loop.

# replace audio
# https://superuser.com/questions/1137612/ffmpeg-replace-audio-in-video
# You will want to copy the video stream without re-encoding to save a lot of time but re-encoding the audio might help
# to prevent incompatibilities:
#
# ffmpeg -i v.mp4 -i a.wav -c:v copy -map 0:v:0 -map 1:a:0 new.mp4
# -map 0:v:0 maps the first (index 0) video stream from the input to the first (index 0) video stream in the output.
#
# -map 1:a:0 maps the second (index 1) audio stream from the input to the first (index 0) audio stream in the output.
#
# If the audio is longer than the video, you will want to add -shortest before the output file name.
#
# Not specifying an audio codec, will automatically select a working one.
# You can specify one by for example adding -c:a libvorbis after -c:v copy.

REAL_TIME_OUTPUT = True


def process(source_folder, target_folder):
    i = 1
    for root, dirs, files in os.walk(source_folder):
        for file_name in files:
            command_in = os.path.join(root, file_name)

            if file_name[0] == '.':
                os.remove(command_in)
                continue

            time_now = time.strftime("%H-%M-%S ", time.localtime())
            command_out = os.path.join(target_folder, os.path.splitext(file_name)[0] + '.mp4')

            # 直接转换成为 mp4
            command_mp4 = "ffmpeg -i \"{0}\" \"{1}\"".format(command_in, command_out)

            # 顺时针90度
            command_rotate = "ffmpeg -i \"{0}\" -vf \"transpose=1\" \"{1}\"".format(
                command_in, command_out)

            # 修改对比度 以及 截取时间
            command_contrast = "ffmpeg -i \"{0}\" -ss 10 -t 3 -vf \"eq=contrast=1.6\" \"{1}\"".format(
                command_in, command_out)

            # 修改 Gamma
            command_gamma = "ffmpeg -i \"{0}\" -vf \"eq=gamma=1.65\" \"{1}\"".format(
                command_in, command_out)

            command_real = command_rotate

            if REAL_TIME_OUTPUT:
                my_process = subprocess.Popen(command_real, stdout=subprocess.PIPE,
                                              stderr=subprocess.STDOUT,
                                              universal_newlines=True, encoding='utf-8')
                while True:
                    for line in my_process.stdout:
                        print('Converting: {0} -> {1}'.format(i, line))
                    break
            else:
                os.system(command_real)
            print('Process: ', i, ' completed.')
            i = i + 1


if __name__ == "__main__":
    source_folder = r'D:\1'
    target_folder = source_folder + '_done'
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    process(source_folder, target_folder)
