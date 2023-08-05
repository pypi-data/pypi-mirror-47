import requests
import random
import math
from Crypto.Cipher import AES
import base64
import codecs
import os
from ybc_exception import *


# IP代理池
def _get_ip_list(url, userAgent):
    session = requests.Session()
    session.headers['user-agent'] = userAgent
    htmls = session.get(url).text

    root_pattren = 'alt="Cn" /></td>([\d\D]*?)</tr>'
    root = re.findall(root_pattren, htmls)
    list_ip = []

    for i in range(len(root)):
        key = re.findall('<td>([\d\D]*?)</td>', root[i])
        list_ip.append(key[3].lower() + '://' + key[0] + ':' + key[1])
    return list_ip


def _get_random_id(list_ip):
    list_proxy = list_ip
    proxy = random.choice(list_proxy)
    if 'https' in proxy:
        return {'https': proxy}
    return {'http': proxy}


def _get_proxy():
    url = 'http://www.xicidaili.com/wt/'
    userAgent = 'Mozilla/5.0 (Windows NT 10.0; WOW64)'
    list_ip = _get_ip_list(url, userAgent)
    proxy = _get_random_id(list_ip)
    return proxy


class Spider(object):
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
            'Cookie': '_iuqxldmzr_=32; _ntes_nnid=8d4ef0883a3bcc9d3a2889b0bf36766a,1533782432391; _ntes_nuid=8d4ef0883a3bcc9d3a2889b0bf36766a; __utmc=94650624; WM_TID=GzmBlbRkRGQXeQiYuDVCfoEatU6VSsKC; playerid=19729878; __utma=94650624.1180067615.1533782433.1533816989.1533822858.9; __utmz=94650624.1533822858.9.7.utmcsr=cn.bing.com|utmccn=(referral)|utmcmd=referral|utmcct=/; WM_NI=S5gViyNVs14K%2BZoVerGK69gLlmtnH5NqzyHcCUY%2BiWm2ZaHATeI1gfsEnK%2BQ1jyP%2FROzbzDV0AyJHR4YQfBetXSRipyrYCFn%2BNdA%2FA8Mv80riS3cuMVJi%2BAFgCpXTiHBNHE%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6ee84b674afedfbd3cd7d98b8e1d0f554f888a4abc76990b184badc4f89e7af8ece2af0fea7c3b92a91eba9b7ec738e8abdd2b741e986a1b7e87a8595fadae648b0b3bc8fcb3f8eafb69acb69818b97ccec5dafee9682cb4b98bb87d2e66eb19ba2acaa5bf3b6b7b1ae5a8da6ae9bc75ef49fb7abcb5af8879f87c16fb8889db3ec7cbbae97a4c566e992aca2ae4bfc93bad9b37aab8dfd84f8479696a7ccc44ea59dc0b9d7638c9e82a9c837e2a3; JSESSIONID-WYYY=sHwCKYJYxz6ODfURChA471BMF%5CSVf3%5CTc8Qcy9h9Whj6CfMxw4YWTMV7CIx5g6rqW8OBv04YGHwwq%2B%5CD1N61qknTP%2Fym%2BHJZ1ylSH1EabbQASc9ywIT8YvOr%2FpMgvmm1cbr2%2Bd6ssMYXuTlpOIrKqp%5C%2FM611EhmfAfU47%5CSQWAs%2BYzgY%3A1533828139236'

        }

    def __get_songs(self, name):
        d = '{"hlpretag":"<span class=\\"s-fc7\\">","hlposttag":"</span>","s":"%s","type":"1","offset":"0","total":"true","limit":"30","csrf_token":""}' % name
        wyy = WangYiYun(d)  # 要搜索的歌曲名在这里
        data = wyy.get_data()
        url = 'https://music.163.com/weapi/cloudsearch/get/web?csrf_token='
        response = requests.post(url, data=data, proxies=_get_proxy(), headers=self.headers).json()
        # print(response)
        return response['result']

    def __get_mp3(self, id):
        d = '{"ids":"[%s]","br":320000,"csrf_token":""}' % id
        wyy = WangYiYun(d)
        data = wyy.get_data()
        url = 'https://music.163.com/weapi/song/enhance/player/url?csrf_token='
        response = requests.post(url, data=data, proxies=_get_proxy(), headers=self.headers).json()
        return response['data'][0]['url']

    def __download_mp3(self, url, filename, ar):
        """下载mp3"""
        abspath = os.path.abspath('.')  # 获取绝对路径
        os.chdir(abspath)
        response = requests.get(url, headers=self.headers).content
        path = os.path.join(abspath)
        with open(filename + '-' + ar + '.mp3', 'wb') as f:
            f.write(response)
            return str(filename + '-' + ar + '.mp3')

    def __get_ar(self, songs, ar):
        """根据作者筛选歌曲"""
        songs_list = []
        for num, song in enumerate(songs):
            if song['ar'][0]['name'] == ar:
                songs_list.append((song['name'], song['id']))
        return songs_list

    def run(self, name, ar):
        songs = self.__get_songs(name)
        if songs['songCount'] == 0:
            return False
        else:
            songs = self.__get_ar(songs['songs'], ar)
            if len(songs) == 0:
                print("未找到对应的歌曲")
                return -1
            else:
                url = self.__get_mp3(songs[0][1])
                if not url:
                    print("未找到对应的歌曲")
                    return -1
                else:
                    print("歌曲正在加载中，请等待...")
                    filename = songs[0][0]
                    return self.__download_mp3(url, filename, ar)


class WangYiYun(object):
    def __init__(self, d):
        self.d = d
        self.e = '010001'
        self.f = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5a" \
                 "a76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46be" \
                 "e255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
        self.g = "0CoJUm6Qyw8W8jud"
        self.random_text = self.get_random_str()

    def get_random_str(self):
        """js中的a函数"""
        str = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        res = ''
        for x in range(16):
            index = math.floor(random.random() * len(str))
            res += str[index]
        return res

    def aes_encrypt(self, text, key):
        iv = '0102030405060708'  # 偏移量
        pad = 16 - len(text.encode()) % 16  # 使加密信息的长度为16的倍数，要不会报下面的错
        # 长度是16的倍数还会报错，不能包含中文，要对他进行unicode编码
        text = text + pad * chr(pad)  # Input strings must be a multiple of 16 in length
        encryptor = AES.new(key, AES.MODE_CBC, iv)
        msg = base64.b64encode(encryptor.encrypt(text))  # 最后还需要使用base64进行加密
        return msg

    def rsa_encrypt(self, value, text, modulus):
        '''进行rsa加密'''
        text = text[::-1]
        rs = int(codecs.encode(text.encode('utf-8'), 'hex_codec'), 16) ** int(value, 16) % int(modulus, 16)
        return format(rs, 'x').zfill(256)

    def get_data(self):
        # 这个参数加密两次
        params = self.aes_encrypt(self.d, self.g)
        params = self.aes_encrypt(params.decode('utf-8'), self.random_text)
        enc_sec_key = self.rsa_encrypt(self.e, self.random_text, self.f)
        return {
            'params': params,
            'encSecKey': enc_sec_key
        }


@exception_handler('ybc_music')
@params_check([
    ParamCheckEntry('name', str, is_not_empty),
    ParamCheckEntry('ar', str, is_not_empty)
])
def search_music(name, ar):
    spider = Spider()
    res = spider.run(name, ar)
    return res


if __name__ == '__main__':
    print(search_music('结果', '花儿乐队'))
