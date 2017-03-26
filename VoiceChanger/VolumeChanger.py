#coding:UTF-8
import sys
import os
import struct
import wave
import random
from glob import *
from scipy import *

global params
global nchannels, sample_width, framerate, num_frame
global speaker_name
global audio_name
global volume_minus_left, volume_minus_right, volume_add_left, volume_add_right

#音频音量系数
volume_minus_left = 0
volume_minus_right = 1

volume_add_left = 1
volume_add_right = 5

global uniform_decrease_num, uniform_increase_num
#每帧变化相同比率
uniform_decrease_num = 10  # 衍生减小音量的音频数目
uniform_increase_num = 10  # 衍生增大音量的音频数目

global not_uniform_decrease_num, not_uniform_increase_num
#每帧变化不同比率
not_uniform_decrease_num = 50  # 衍生减小音量的音频数目
not_uniform_increase_num = 50  # 衍生增大音量的音频数目

#输入错误提示信息
def printError():
    print('Error.')
    print('Usage: $ python Spectrogram1.py <wav sound file folder> <new wav save folder>')
    sys.exit()


#改变音量
#参数1:若降低音量则为True，若增加音量则为False
#参数2:衍生音频数量
#参数3:衍生音频起始数
def changeVolumeValue(uniform,decrease,num_total,num_start):
    global volume_add_left, volume_add_right, volume_minus_left, volume_minus_right
    global framerate, num_frame

    if(uniform):
        if (decrease):
            radio = random.uniform(volume_minus_left, volume_minus_right)
        else:
            radio = random.uniform(volume_add_left, volume_add_right)

    count = num_start

    for i in range(num_total):
        if (not os.path.exists(sys.argv[2] + speaker_name)):
            os.mkdir(sys.argv[2] + speaker_name)

        amplitude_audio = wave.open(sys.argv[2] + speaker_name + '/' + audio_name + '_volume_' + str(count) + '.wav',
                                    'wb')
        count = count + 1
        amplitude_params = [1, 2, framerate, num_frame, params[4], params[5]]
        amplitude_audio.setparams(amplitude_params)
        audio_new_bytes = ""

        for j in range(num_frame):
            if (not uniform):
                if (decrease):
                    radio = random.uniform(volume_minus_left, volume_minus_right)
                else:
                    radio = random.uniform(volume_add_left, volume_add_right)

            value = short(volume[j] * radio)
            byte = struct.pack('h', value)
            audio_new_bytes = audio_new_bytes + byte

        amplitude_audio.writeframes(audio_new_bytes)
        amplitude_audio.close()


#改变音频响度
def changeVolume(audio_path):
    audio = wave.open(audio_path)
    global params
    params = audio.getparams()
    global nchannels, sample_width, framerate, num_frame
    nchannels, sample_width, framerate, num_frame = params[:4]

    global volume
    volume = zeros(num_frame)
    for i in range(num_frame):
        val = audio.readframes(1)
        value = struct.unpack('h', val)[0]
        volume[i] = value
    audio.close()

    #每帧改变相同的比率
    global uniform_decrease_num, uniform_increase_num
    global not_uniform_decrease_num, not_uniform_increase_num


    uniform_decrease_start = 0#每帧降低相同比率起始音频index
    uniform_increase_start = uniform_decrease_num+uniform_decrease_start#每帧升高相同比率起始音频index

    changeVolumeValue(True,True,uniform_decrease_num,uniform_decrease_start)
    changeVolumeValue(True,False,uniform_increase_num,uniform_increase_start)

    #每帧改变不同的比率
    not_uniform_decrease_start = uniform_increase_start + uniform_increase_num#每帧降低不同比率起始音频index
    not_uniform_increase_start = not_uniform_decrease_start + not_uniform_decrease_num#每帧升高不同比率起始音频index

    changeVolumeValue(False, True, not_uniform_decrease_num, not_uniform_decrease_start)
    changeVolumeValue(False, False, not_uniform_increase_num, not_uniform_increase_start)


def getWavFiles():
    # 读取所有wav音频文件
    #files_dir = glob("/Users/zhangjingjing/Documents/study/IsolatedWordRecognition/data/wav/1_ZJJ_8k/*.wav")
    files_dir = glob(sys.argv[1]+'*')
    # audio = wave.open("/Users/zhangjingjing/Documents/study/IsolatedWordRecognition/data/1_ZJJ_41k/0-1.wav","rb")
    for file_dir in files_dir:
        global speaker_name
        speaker_name = file_dir.split('/')[-1]
        #print speaker_name

        subfiles_dir = glob(file_dir+'/*')

        for subfile_dir in subfiles_dir:
            global audio_name
            audio_name = subfile_dir.split('/')[-1][:-4]
            changeVolume(subfile_dir)


#两个参数
#参数1:音频存储目录 "/Users/zhangjingjing/Documents/study/IsolatedWordRecognition/data/wav/fruits/train/"
#train目录下是文件夹，每个文件夹下是wav文件
#参数2:生成音频保存目录
#/Users/zhangjingjing/Documents/study/IsolatedWordRecognition/data/wav/fruits/volume_changed/
def main():
    # Makes sure we have been given proper input.
    if len(sys.argv) != 3:
        printError()

    getWavFiles()



if __name__== '__main__':
    main()