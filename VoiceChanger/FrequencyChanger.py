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
global frame_minus_left, frame_minus_right, frame_add_left, frame_add_right
global step


#将多少帧分为一组处理
step = 100


#音频帧数减少
frame_minus_left = 1
frame_minus_right = step/3

#音频帧数增加
frame_add_left = 1
frame_add_right = step/3

#输入错误提示信息
def printError():
    print('Error.')
    print('Usage: $ python Spectrogram1.py <wav sound file folder> <new wav save folder>')
    sys.exit()


#增加帧数，降低频率
#参数1:衍生音频数量
#参数2:衍生音频起始数
def decreaseFrequency(num_total,num_start):
    global radio_minus_left,radio_minus_right
    global framerate, num_frame
    global step
    count = num_start

    for i in range(num_total):
        if(not os.path.exists(sys.argv[2]+speaker_name)):
            os.mkdir(sys.argv[2]+speaker_name)

        frame_add = random.randint(frame_add_left,frame_add_right)
        print 'add ' + str(frame_add)

        frequency_audio = wave.open(sys.argv[2]+speaker_name+'/'+audio_name + '_frequency_' + str(count) + '.wav','wb')
        count = count + 1
        audio_new_bytes = ""

        quotient = num_frame/step
        remainder = num_frame%step

        num_frame_new = 0

        #每个step中随机选取frame_add个要复制的帧
        for j in range(quotient):
            #随机选取frame_add个复制帧
            frame_copy = []
            while(True):
                if(frame_copy.__len__() >= frame_add):
                    break;
                index = random.randint(0, step)
                if index in frame_copy:
                    continue
                else:
                    frame_copy.append(index)

            frame_copy.sort()#从小到大排序
            print frame_copy
            current_copy_index = frame_copy[0]#current_copy_index是当前待复制帧下标

            for k in range(step):
                value = volume[j*step+k]
                byte = struct.pack('h',value)
                audio_new_bytes = audio_new_bytes + byte
                num_frame_new = num_frame_new + 1
                if(k == current_copy_index):
                    audio_new_bytes = audio_new_bytes + byte
                    num_frame_new = num_frame_new + 1
                    del frame_copy[0]
                    if(frame_copy.__len__()>0):
                        current_copy_index = frame_copy[0]


        '''
        #复制前frame_add帧的内容
        for j in range(quotient):
            for k in range(step):
                value = volume[j*step+k]
                byte = struct.pack('h',value)
                audio_new_bytes = audio_new_bytes + byte
                num_frame_new = num_frame_new + 1
                if(k <= frame_add):
                    audio_new_bytes = audio_new_bytes + byte
                    num_frame_new = num_frame_new + 1'''


        for k in range(remainder):
            value = volume[quotient * step + k]
            byte = struct.pack('h', value)
            audio_new_bytes = audio_new_bytes + byte
            num_frame_new = num_frame_new + 1
            if (k <= frame_add):
                audio_new_bytes = audio_new_bytes + byte
                num_frame_new = num_frame_new + 1


        print num_frame, num_frame_new
        frequency_params = [1, 2, framerate, num_frame_new, params[4], params[5]]
        frequency_audio.setparams(frequency_params)
        frequency_audio.writeframes(audio_new_bytes)
        frequency_audio.close()


#减少帧数，提高频率
#参数1:衍生音频数量
#参数2:衍生音频起始数
def increaseFrequency(num_total,num_start):
    global frame_add_left, frame_add_right
    global step
    count = num_start


    for i in range(num_total):
        if(not os.path.exists(sys.argv[2]+speaker_name)):
            os.mkdir(sys.argv[2]+speaker_name)

        frame_minus = random.randint(frame_minus_left, frame_minus_right)
        print 'minus ' + str(frame_minus)

        frequency_audio = wave.open(sys.argv[2]+speaker_name+'/'+audio_name + '_frequency_' + str(count) + '.wav','wb')
        count = count + 1
        audio_new_bytes = ""

        quotient = num_frame/step
        remainder = num_frame%step

        num_frame_new = 0

        # 每个step中随机选取frame_minus个要删除的帧
        for j in range(quotient):
            #随机要删除的帧
            frame_delete = []
            while(True):
                if(frame_delete.__len__() >= frame_minus):
                    break;
                index = random.randint(0, step)
                if index in frame_delete:
                    continue
                else:
                    frame_delete.append(index)

            frame_delete.sort()#从小到大排序
            print frame_delete
            current_delete_index = frame_delete[0]#current_delete_index是当前待删除帧下标

            for k in range(step):
                if(k == current_delete_index):
                    del frame_delete[0]
                    if (frame_delete.__len__() > 0):
                        current_delete_index = frame_delete[0]
                    continue
                else:
                    value = volume[j * step + k]
                    byte = struct.pack('h',value)
                    audio_new_bytes = audio_new_bytes + byte
                    num_frame_new = num_frame_new + 1

        '''
        #每个step中删除前frame_add个偶数帧
        for j in range(quotient):
            for k in range(step):
                if((k%2 == 0) and (k/2 <= frame_minus)):
                    continue
                else:
                    value = volume[j * step + k]
                    byte = struct.pack('h',value)
                    audio_new_bytes = audio_new_bytes + byte
                    num_frame_new = num_frame_new + 1
        '''

        #删除前frame_add个偶数帧
        for k in range(remainder):
            if ((k % 2 == 0) and (k / 2 <= frame_minus)):
                continue
            else:
                value = volume[quotient * step + k]
                byte = struct.pack('h', value)
                audio_new_bytes = audio_new_bytes + byte
                num_frame_new = num_frame_new + 1

        print num_frame, num_frame_new
        frequency_params = [1, 2, framerate, num_frame_new, params[4], params[5]]
        frequency_audio.setparams(frequency_params)
        frequency_audio.writeframes(audio_new_bytes)
        frequency_audio.close()



#改变音频响度
def changeFrequency(audio_path):
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

    decrease_num = 1#衍生减小音量的音频数据
    decrease_start = 0#从标号为decrease_start开始标记
    decreaseFrequency(decrease_num,decrease_start)

    increase_num = 1#衍生增大音量的音频数目
    increaseFrequency(increase_num,decrease_num+decrease_start)



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
            changeFrequency(subfile_dir)


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