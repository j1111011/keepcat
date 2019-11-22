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
# 百度语音的key.
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
    
def record(path):
    os.system('arecord -D "plughw:1,0" -f S16_LE -r 16000 -d 20 ' + path)
    
def main():
    global completed
    r = random.uniform(0.8,8.8)
    time.sleep(r)
    wakeup = '天猫精灵'
    dingdang = '冲鸭打卡'
    logging.info('play: ' + wakeup)
    play(wakeup,'tmjl')
    logging.info('sleep ~')
    time.sleep(0.8)
    logging.info('play: ' + dingdang)
    play(dingdang,'cydk')
    #os.system('play ' + work_dir + '/cydk.wav')
    file = work_dir + '/caches/' + time.strftime("%Y-%m-%d-%H_%M_%S",time.localtime(time.time())) + '_says.wav'
    record(file)
    says = get_file_content(file)
    key = ''
    #pattern = u'\u53e3\u4ee4\u5929\u732b\u7cbe\u7075(\S*)\u8be6\u7ec6\u4efb\u52a1'
    pattern = [u'\S*\u7cbe\u7075(\S*)\u8be6\u7ec6',
                u'\S*\u5bf9\u6211\u8bf4(\S*)\u8be6\u7ec6']
    for p in pattern:
        pat = re.compile(p)
        result = pat.findall(says)
        if len(result) > 0:
            key = pat.findall(says)[0]
            if len(key) > 0:
                break
    if len(key) <= 0:
       pattern2 = u'\u5df2\u5b8c\u6210'
       pat2 = re.compile(pattern2)
       res2 = pat2.findall(says)
       #key = get_emotibot(says)
       if len(res2) > 0:
            completed = True
            play('今天的冲鸭打卡任务已完成','wc')
            logging.info('今天的任务已完成')
    else:
        logging.info('key: ' + key)
        play(key,'xzjd',False,True)
        play(wakeup,'tmjl')
        time.sleep(1)
        play(key,'xzjd')

    #s = get_emotibot(sys.argv[1])
    #save(s)
    
if __name__ == "__main__":
    for _ in range(0,10):
        if completed == False:
                    try:
                        main()
                    except Exception as err:
                        logging.error(err)
