# Keepcat 另类养猫之旅

1. 使用的是百度ASR,TTS。需要[申请aip key.](https://console.bce.baidu.com/ai/?_=1574388926562&fromai=1#/ai/speech/overview/index)

2. 我使用的是arecord来录音，我使用提USB麦克风。这里需要使用-D  "plughw:1,0" 来指定录音设备

`def record():`
`    os.system('arecord -D "plughw:1,0" -f S16_LE -r 16000 -d 20 ' + path)`

3. keepcat.py 对话，并从对话中查找关键字。
4. says.py 补充对话
5. 使用python3运行，需要安装pip3 install baidu-aip
6. 可以配合homeassistant使用，将ha目录直接放到.homeassistant/packages/就可以使用了。注意修改你keepcat脚本的路径
7. 使用play,arecord来录音，系统必须有这2个命令

