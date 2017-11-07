from urllib.request import Request,urlopen
import codecs
def processCallBack(bn, bs, ts):
    f = lambda x: round(x / 1024 / 1024, 2)
    res = list(map(f, [ts, bn * bs]))
    res.append(round(bn * bs / ts * 100, 2))
    print("{0[0]}/{0[1]},{0[2]}".format(res))

def download(url, filename):
    bs = 1024 * 10
    read = 0
    headers = {'Accept': '*/*',
               'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
               'Connection': 'keep-alive',
               'Host': 'cdn.media.hostedtube.com',
               'Upgrade-Inscure-Requests': 1,
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3159.5 Safari/537.36',
               'Referer': 'http://www.jizzkontu.com/?qqdrsign=03861'}

    req = Request(url=url)
    http_fp = urlopen(req)
    print(http_fp.getheader("Content-Length"))
    while True:
        block = http_fp.read(bs)
        read += len(block)
        if not http_fp:
            break
        with codecs.open(filename, 'wb') as fp:
            fp.write(block)
        print(block)

url = 'http://blog.csdn.net/bo_mask/article/details/76067790'
filename = 'a.html'
download(url, filename)