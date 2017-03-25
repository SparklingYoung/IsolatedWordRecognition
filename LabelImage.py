#coding:UTF-8
import sys

from glob import *


#返回声谱图名称
def getSpecgramName(file_dir):
    specgram_name = file_dir.split('/')[-1]
    return specgram_name

#返回声谱图对应的label值
def getLabelValue(specgram_name):
    label = (specgram_name.split('_')[2]).split('-')[0]
    return int(label) - 1



#对声谱图打label
def labelIt(label_file):
    files_dir = glob(sys.argv[1] + '*')

    for file_dir in files_dir:
        specgram_name = getSpecgramName(file_dir)
        label = getLabelValue(specgram_name)

        #保存label信息
        label_file.write(specgram_name + ' ' + str(label) + '\n')



def printError():
    print('Error.')
    print('Usage: $ python Spectrogram.py <specgram files folder> <label text save folder>')
    sys.exit()


#两个参数
#参数1:声谱图路径
#参数2:保存声谱图label信息txt存储路径
def main():
    if(len(sys.argv) != 3):
        printError()


    label_file = open(sys.argv[2]+'label.txt','w')
    labelIt(label_file)
    label_file.close()


if __name__ == '__main__':
    main()
