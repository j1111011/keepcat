# -*- coding: utf-8 -*-

import requests
import json
import sys
import time
import os
import re
import random
from aip import AipSpeech
import logging
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"    # 日志格式化输出
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"                        # 日期格式
fp = logging.FileHandler(sys.path[0] + '/keepcat.log', encoding='utf-8')
fs = logging.StreamHandler()
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, datefmt=DATE_FORMAT, handlers=[fp, fs])    # 调用
userid = ''
completed = False
work_dir = sys.path[0]
# 填写你申请的百度语音的key.
api_key = ''
secret_key = ''

def save(msg,path):
    app_id = '17090394'
    client = AipSpeech(app_id,api_key,secret_key)
    result = client.synthesis(msg,'zh',1,{'vol':9,'per':1})
    logging.info(path)
    f = open(path,'wb')
    f.write(result)
    f.close()
    
# 1.将wma格式文件转为pcm格式文件
def get_file_content(filePath):
    # 执行cmd命令os.system()
    # os.system(f"ffmpeg -y  -i {filePath} -acodec pcm_s16le -f s16le -ac 1 -ar 16000 {filePath}.pcm")
    fp = open(filePath, 'rb')
    content = fp.read()
    app_id = '17090394'
    client = AipSpeech(app_id,api_key,secret_key)
    # 2.将音频转成文字
    res = client.asr(content, 'pcm', 16000, {
    # 不填写lan参数生效,都不填写,默认1537(普通话 输入法模型),dev_pid参数见本节开头的表格
        'dev_pid': 1536,
    })
    logging.info(res)
    return res.get('result')[0]

def play(msg,filename,playIt=True,update=False):
    path = work_dir + '/' + filename + '.mp3'
    if os.path.exists(path) == False or update:
        save(msg,path)
    if playIt:
        os.system('play ' + path)
    

def say():
    wakeup = '天猫精灵'
    say = sys.argv[1]
    logging.info('say: ' + say)
    play(wakeup,'tmjl')
    time.sleep(0.8)
    play(say,'says',True,True)

if __name__ == "__main__":
    say()
