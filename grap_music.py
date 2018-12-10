# 爬取QQ音乐音乐排行榜中“巅峰榜.流行指数”前100首歌的信息
# -*-coding:utf-8 -*-

# Request URL: https://c.y.qq.com/v8/fcg-bin/fcg_v8_toplist_cp.fcg?tpl=3&page=detail&date=2018-12-09&topid=4&type=top&song_begin=0&song_num=30&g_tk=5381&jsonpCallback=MusicJsonCallbacktoplist&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0

import requests
import json

url = 'https://c.y.qq.com/v8/fcg-bin/fcg_v8_toplist_cp.fcg?tpl=3&page=detail&date=2018-12-09&topid=4&type=top&song_begin=0&song_num=30&g_tk=5381&jsonpCallback=MusicJsonCallbacktoplist&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0'
res = requests.get(url)  # 获取数据
jd = json.loads(res.text.replace('MusicJsonCallbacktoplist(', '').rstrip(')'))  # 将获取的数据，去掉头部分"MusicJsonCallbacktoplist("和尾部分"）"，转成json数据
for item in jd['songlist']:
    name_list = ''
    singer_num = 0  # 歌手的数量
    # 因为同一首歌可能存在多个歌手名,所以，把歌手名用字符串拼接起来
    for singer_name in item['data']['singer']:
        if(singer_num == 0):
            name_list = name_list + singer_name['name']
        else:
            name_list = name_list + '，' + singer_name['name']
        singer_num = singer_num + 1  # 歌手数量加1

    print(item['data']['albumname'], item['data']['songname'], name_list)  # 专辑名，歌曲名

