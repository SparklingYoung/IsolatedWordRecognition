#coding: UTF-8
import wave
import struct

from scipy import *


radio = 0.5

#读取原始音频文件
audio = wave.open("/Users/zhangjingjing/Documents/study/IsolatedWordRecognition/data/1_ZJJ_8k/0-1.wav","rb")
#写入时间压缩扩张音频文件
half_time_audio = wave.open("/Users/zhangjingjing/Documents/study/IsolatedWordRecognition/data/1_ZJJ_8k/0-1-ht.wav","wb")
double_time_audio = wave.open("/Users/zhangjingjing/Documents/study/IsolatedWordRecognition/data/1_ZJJ_8k/0-1-dt.wav","wb")
#写入采样率改变的音频文件
framerate_audio = wave.open("/Users/zhangjingjing/Documents/study/IsolatedWordRecognition/data/1_ZJJ_8k/0-1-" + str(radio) + "f.wav","wb")
#写入振幅改变的音频文件
amplitude_audio = wave.open("/Users/zhangjingjing/Documents/study/IsolatedWordRecognition/data/1_ZJJ_8k/0-1-" + str(radio) + "a.wav","wb")

#获取音频文件相关参数
params = audio.getparams()
nchannels, sample_width, framerate, num_frame = params[:4]

#提取音频文件中每帧对应的值，存储至volume中
volume = zeros(num_frame)
for i in range(num_frame):
    val = audio.readframes(1)
    value = struct.unpack('h',val)[0]
    volume[i] = value
    print "original", i, value
audio.close()


#------------------------------------------时间--------------------------------------------
#将音频时间减半
half_time_params = [1,2,framerate,num_frame/2,params[4],params[5]]
half_time_audio.setparams(half_time_params)
half_time_bytes = ""

for i in range(num_frame/2):
    value = short(volume[2*i])
    byte = struct.pack('h',value)
    half_time_bytes = half_time_bytes+byte

half_time_audio.writeframes(half_time_bytes)
half_time_audio.close()


#将音频时间加倍
double_time_params = [1,2,framerate,num_frame*2-1,params[4],params[5]]
double_time_audio.setparams(double_time_params)
double_time_bytes = ""

for i in range(num_frame*2 - 1):
    value = short((volume[i/2]+volume[(i+1)/2])/2)
    byte = struct.pack('h',value)
    double_time_bytes = double_time_bytes+byte

double_time_audio.writeframes(double_time_bytes)
double_time_audio.close()



#------------------------------------------振幅--------------------------------------------
if(radio <= 1):
    amplitude_params = [1,2,framerate,num_frame,params[4],params[5]]
    amplitude_audio.setparams(amplitude_params)
    amplitude_bytes = ""

    for i in range(num_frame):
        value = short(volume[i]*radio)
        byte = struct.pack('h',value)
        amplitude_bytes = amplitude_bytes+byte

    amplitude_audio.writeframes(amplitude_bytes)
    amplitude_audio.close()

#------------------------------------------频率--------------------------------------------
framerate_params = [1,2,int(framerate*radio),num_frame,params[4],params[5]]
framerate_audio.setparams(framerate_params)
print framerate_params
framerate_bytes = ""

for i in range(num_frame):
    value = short(volume[i])
    byte = struct.pack('h',value)
    framerate_bytes = framerate_bytes+byte

framerate_audio.writeframes(framerate_bytes)
framerate_audio.close()