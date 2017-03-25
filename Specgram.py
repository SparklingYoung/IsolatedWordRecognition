#coding: UTF-8
import wave
import struct

from glob import *
from pylab import *


#保存得到的声谱图
def saveSpecgram(speaker_name,audio_name):
    #show()
    dst_path = sys.argv[2]+speaker_name + '_' + audio_name +'.jpg'
    savefig(dst_path)
    close()



#声谱图处理
def getSpecgram(path):
    # 返回wav音频参数，返回值为一个元组
    # 元组为：声道数，量化位数(byte)，采样率，采样点数，压缩类型，压缩类型的描述
    audio = wave.open(path)
    params = audio.getparams()
    nchannels, sample_width, framerate, num_frames = params[:4]

    volume = zeros(num_frames)

    for i in range(num_frames):
        val = audio.readframes(1)[0:2]
        value = struct.unpack('h', val)[0]  # 将string转换为short类型数
        volume[i] = value

    audio.close()


    # NTTF是FFT的长度，越长的话，频域分辨率越高，但是对于语音这种时变信号，不能过长，一般采样率16k或8k的取
    # 1024或512，要看采样率的高低
    # noverlap是指NTTF减去步长，越大越好，但运算量大，一般取NTTF的3/4即可
    specgram(volume, NFFT=512, Fs=framerate, noverlap=384)
    axis("off")

    speaker_name = path.split('/')[-2]
    audio_name = path.split('/')[-1][:-4]
    #print speaker_name, audio_name
    saveSpecgram(speaker_name,audio_name)
    #save("/Users/zhangjingjing/Documents/study/IsolatedWordRecognition/data/1_ZJJ_8k/1.jpg",d)




#获取指定目录下的所有wav文件
def getWavFiles():
    # 读取所有wav音频文件
    #files_dir = glob("/Users/zhangjingjing/Documents/study/IsolatedWordRecognition/data/wav/1_ZJJ_8k/*.wav")
    files_dir = glob(sys.argv[1]+'*')
    # audio = wave.open("/Users/zhangjingjing/Documents/study/IsolatedWordRecognition/data/1_ZJJ_41k/0-1.wav","rb")
    for file_dir in files_dir:
        #speaker_name = file_dir.split('/')[-1]
        #print speaker_name

        subfiles_dir = glob(file_dir+'/*')

        for subfile_dir in subfiles_dir:
            #audio_name = subfile_dir.split('/')[-1]
            #print audio_name
            getSpecgram(subfile_dir)

        #


#输入错误提示信息
def printError():
    print('Error.')
    print('Usage: $ python Spectrogram.py <wav sound file folder> <specgram save folder>')
    sys.exit()


#两个参数
#参数1:音频存储目录
#参数2:生成声谱图存储目录
def main():
    # Makes sure we have been given proper input.
    if len(sys.argv) != 3:
        printError()

    getWavFiles()



if __name__== '__main__':
    main()