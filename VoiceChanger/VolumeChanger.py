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
uniform_decrease_num = 1  # 衍生减小音量的音频数目 10
uniform_increase_num = 1  # 衍生增大音量的音频数目 10

global not_uniform_decrease_num, not_uniform_increase_num
#每帧变化不同比率
not_uniform_decrease_num = 1  # 衍生减小音量的音频数目 50
not_uniform_increase_num = 1  # 衍生增大音量的音频数目 50

#输入错误提示信息
def printError():
    print('Error.')
    print('Usage: $ python Spectrogram1.py <wav sound file folder> <new wav save folder>')
    sys.exit()





##########################################uniformDecreaseVolume########################################
# 统一方式降低音量，每帧的音量改变的比率相同
# 参数1:衍生音频数量
# 参数2:衍生音频起始数
def uniformDecreaseVolume(num_total, num_start):
    print "uniformDecreaseVolume"
    global volume_minus_left, volume_minus_right
    global framerate, num_frame

    radio = random.uniform(volume_minus_left, volume_minus_right)

    count = num_start

    for i in range(num_total):
        if (not os.path.exists(sys.argv[2] + speaker_name)):
            os.mkdir(sys.argv[2] + speaker_name)

        amplitude_audio = wave.open(
            sys.argv[2] + speaker_name + '/' + audio_name + '_volume_' + str(count) + '.wav',
            'wb')
        count = count + 1
        amplitude_params = [1, 2, framerate, num_frame, params[4], params[5]]
        amplitude_audio.setparams(amplitude_params)
        audio_new_bytes = ""

        for j in range(num_frame):
            value = short(volume[j] * radio)
            byte = struct.pack('h', value)
            audio_new_bytes = audio_new_bytes + byte

        amplitude_audio.writeframes(audio_new_bytes)
        amplitude_audio.close()





##########################################uniformIncreaseVolume########################################
# 统一方式提高音量，每帧的音量改变的比率相同
# 参数1:衍生音频数量
# 参数2:衍生音频起始数
def uniformIncreaseVolume(num_total,num_start):
    print "uniformIncreaseVolume"
    global volume_add_left, volume_add_right
    global framerate, num_frame

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
            value = short(volume[j] * radio)
            byte = struct.pack('h', value)
            audio_new_bytes = audio_new_bytes + byte

        amplitude_audio.writeframes(audio_new_bytes)
        amplitude_audio.close()







##########################################notUniformDecreaseVolume########################################
# 非统一方式降低音量，每帧的音量改变的比率不同
# 参数1:衍生音频数量
# 参数2:衍生音频起始数
def notUniformDecreaseVolume(num_total, num_start):
    print "notUniformDecreaseVolume"
    global volume_minus_left, volume_minus_right
    global framerate, num_frame


    count = num_start

    for i in range(num_total):
        if (not os.path.exists(sys.argv[2] + speaker_name)):
            os.mkdir(sys.argv[2] + speaker_name)

        amplitude_audio = wave.open(
            sys.argv[2] + speaker_name + '/' + audio_name + '_volume_' + str(count) + '.wav',
            'wb')
        count = count + 1
        amplitude_params = [1, 2, framerate, num_frame, params[4], params[5]]
        amplitude_audio.setparams(amplitude_params)
        audio_new_bytes = ""

        for j in range(num_frame):
            radio = random.uniform(volume_minus_left, volume_minus_right)
            value = short(volume[j] * radio)
            byte = struct.pack('h', value)
            audio_new_bytes = audio_new_bytes + byte

        amplitude_audio.writeframes(audio_new_bytes)
        amplitude_audio.close()







##########################################notUniformIncreaseVolume########################################
# 非统一方式提高音量，每帧的音量改变的比率不同
# 参数1:衍生音频数量
# 参数2:衍生音频起始数
def notUniformIncreaseVolume(num_total, num_start):
    print "notUniformIncreaseVolume"
    global volume_add_left, volume_add_right
    global framerate, num_frame

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
            radio = random.uniform(volume_add_left, volume_add_right)
            value = short(volume[j] * radio)
            byte = struct.pack('h', value)
            audio_new_bytes = audio_new_bytes + byte

        amplitude_audio.writeframes(audio_new_bytes)
        amplitude_audio.close()







##########################################changeVolumeValue########################################
#改变音量
# 改变帧数，改变频率
# 参数1:每帧音量改变的幅度是否相同，若为True则相同，若为False则不相同
# 参数2:是否是降低音量。若为True，则音量降低；若为False，则音量提高
# 参数3:衍生音频数量
# 参数4:衍生音频起始数
def changeVolumeValue(uniform,decrease,num_total,num_start):
    print "changeVolumeValue"
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


    uniform_decrease_start = 0#每帧降低相同比率起始音频index
    #changeVolumeValue(True,True,uniform_decrease_num,uniform_decrease_start)
    uniformDecreaseVolume(uniform_decrease_num,uniform_decrease_start)
    uniform_increase_start = uniform_decrease_num+uniform_decrease_start#每帧升高相同比率起始音频index
    uniformIncreaseVolume(uniform_increase_num,uniform_increase_start)
    #changeVolumeValue(True,False,uniform_increase_num,uniform_increase_start)


    global not_uniform_decrease_num, not_uniform_increase_num
    #每帧改变不同的比率
    not_uniform_decrease_start = uniform_increase_start + uniform_increase_num#每帧降低不同比率起始音频index
    #changeVolumeValue(False, True, not_uniform_decrease_num, not_uniform_decrease_start)
    notUniformDecreaseVolume(not_uniform_decrease_num,not_uniform_decrease_start)
    not_uniform_increase_start = not_uniform_decrease_start + not_uniform_decrease_num#每帧升高不同比率起始音频index
    #changeVolumeValue(False, False, not_uniform_increase_num, not_uniform_increase_start)
    notUniformIncreaseVolume(not_uniform_increase_num,not_uniform_increase_start)


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