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
volume_add_right = 10

#输入错误提示信息
def printError():
    print('Error.')
    print('Usage: $ python Spectrogram1.py <wav sound file folder> <new wav save folder>')
    sys.exit()


#降低音量
#参数1:衍生音频数量
#参数2:衍生音频起始数
def decreaseVolume(num_total,num_start):
    global radio_minus_left,radio_minus_right
    global framerate, num_frame
    count = num_start

    for i in range(num_total):
        if(not os.path.exists(sys.argv[2]+speaker_name)):
            os.mkdir(sys.argv[2]+speaker_name)

        radio_minus = random.uniform(volume_minus_left,volume_minus_right)
        print radio_minus

        amplitude_audio = wave.open(sys.argv[2]+speaker_name+'/'+audio_name + '_volume_' + str(count) + '.wav','wb')
        count = count + 1
        amplitude_params = [1, 2, framerate, num_frame, params[4], params[5]]
        amplitude_audio.setparams(amplitude_params)
        audio_new_bytes = ""

        for j in range(num_frame):
            value = short(volume[j]*radio_minus)
            byte = struct.pack('h', value)
            audio_new_bytes = audio_new_bytes + byte

        amplitude_audio.writeframes(audio_new_bytes)
        amplitude_audio.close()


#提高音量
#参数1:衍生音频数量
#参数2:衍生音频起始数
def increaseVolume(num_total,num_start):
    global volume_add_left, volume_add_right
    global framerate, num_frame
    count = num_start

    for i in range(num_total):
        if(not os.path.exists(sys.argv[2]+speaker_name)):
            os.mkdir(sys.argv[2]+speaker_name)

        radio_add = random.uniform(volume_add_left, volume_add_right)
        print radio_add

        amplitude_audio = wave.open(sys.argv[2]+speaker_name+'/'+audio_name + '_volume_' + str(count) + '.wav','wb')
        count = count + 1
        amplitude_params = [1, 2, framerate, num_frame, params[4], params[5]]
        amplitude_audio.setparams(amplitude_params)
        audio_new_bytes = ""

        for j in range(num_frame):
            value = short(volume[j]*radio_add)
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

    decrease_num = 5#衍生减小音量的音频数据
    decrease_start = 0#从标号为decrease_start开始标记
    decreaseVolume(decrease_num,decrease_start)

    increase_num = 10#衍生增大音量的音频数目
    increaseVolume(increase_num,decrease_num+decrease_start)



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