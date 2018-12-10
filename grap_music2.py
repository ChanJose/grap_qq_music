# 爬取QQ音乐音乐排行榜中“巅峰榜.流行指数”前100首歌的信息
# 在原有基础上，对代码进行封装
# -*-coding:utf-8 -*-

# Request URL: https://c.y.qq.com/v8/fcg-bin/fcg_v8_toplist_cp.fcg?tpl=3&page=detail&date=2018-12-09&topid=4&type=top&song_begin=0&song_num=30&g_tk=5381&jsonpCallback=MusicJsonCallbacktoplist&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0

import requests
import json
from requests.exceptions import RequestException


# 返回请求链接的text
def get_page(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0(Macintosh;Intel Mac OS X 10_12_6) AppleWebKit/537.36(KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
        }
        response = requests.get(url, headers= headers)  # 请求页面
        if response.status_code == 200:
            return response.text
        else:
            return None
    except RequestException:
        return None


# 分析内容，提取所需的信息
def get_info(response):
    jd = json.loads(response.replace('MusicJsonCallbacktoplist(', '').rstrip(')'))  # 将获取的数据，去掉头部分"MusicJsonCallbacktoplist("和尾部分"）"，转成json数据
    for item in jd['songlist']:
        album_name = item['data']['albumname']  # 专辑名
        song_name = item['data']['songname']  # 歌曲名
        singer_name_list = ''
        singer_num = 0  # 歌手的数量
        # 因为同一首歌可能存在多个歌手名,所以，把歌手名用字符串拼接起来
        for singer_name in item['data']['singer']:
            if(singer_num == 0):
                singer_name_list = singer_name_list + singer_name['name']
            else:
                singer_name_list = singer_name_list + '，' + singer_name['name']
            singer_num = singer_num + 1  # 歌手数量加1
        yield {  #  返回一个生成器对象
            'album_name': album_name,  # 专辑名
            'song_name': song_name,  # 歌曲名
            'singer_name': singer_name_list
        }


# 写入到文件中
def writeToFile(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


# 爬取歌曲信息
def craw(song_begin):
    common_url = 'https://c.y.qq.com/v8/fcg-bin/fcg_v8_toplist_cp.fcg?tpl=3&page=detail&date=2018-12-09&topid=4&type=top&song_begin={}&song_num=30&g_tk=5381&jsonpCallback=MusicJsonCallbacktoplist&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0'  # song_begin那里用了{}
    url = common_url.format(song_begin)  # 组成链接
    response = get_page(url)  # 获取页面text
    info_generator = get_info(response)  # 分析页面，返回存储歌曲信息的生成器对象
    for content in info_generator:
        writeToFile(content)  # 把信息存到文件中


if __name__ == '__main__':
    for i in range(4):
        craw(i * 30)  # 传入每页歌曲开始的数
