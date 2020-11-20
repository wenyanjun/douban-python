'''
@author <coderYJ>
@since <1.0.0>
@QQ群 277030213
@GitHub https://github.com/wenyanjun/douban-python
'''
import requests
from lxml import html
import json
import re
class Douban():

    def __init__(self):
        self.url = ''

    # 获取xpath 元素
    def getHtml(self):
        # 加载网页
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36'}
        r = requests.get(self.url, headers=headers)
        r = str(r.content, 'utf-8')
        et = html.etree
        result = et.HTML(r)
        return result

    # 正在上映
    def nowPlaying(self, city='guangzhou'):
        if city == None:
            city = 'guangzhou'
        # 正在上映
        self.url = 'https://movie.douban.com/cinema/nowplaying/' + str(city)

        result = self.getHtml()
        list = result.xpath('//div[@id="nowplaying"]//ul[@class="lists"]/li')
        arr = []
        for i in list:
            dic = {}
            id = i.xpath('./@id')[0]
            title = i.xpath('./@data-title')[0]
            # 时长
            duration = i.xpath('./@data-duration')[0]
            year = i.xpath('./@data-release')[0]
            region = i.xpath('./@data-region')[0]
            score = i.xpath('./@data-score')[0]
            dic['id'] = id
            dic['title'] = title
            dic['duration'] = duration
            dic['year'] = year
            dic['region'] = region
            dic['score'] = score
            # 图片
            img = i.xpath('./ul/li[@class="poster"]/a/img/@src')[0]
            dic['img'] = img
            arr.append(dic)
        obj = {
            'subject': arr,
            'title': '正在上映',
            'city': city
        }
        return self.json_success(obj)
    # 即将上映
    def upcoming(self, city = 'guangzhou'):
        if city == None:
            city = 'guangzhou'

        self.url = 'https://movie.douban.com/cinema/later/' + str(city)
        result = self.getHtml()
        list = result.xpath('//div[@id="showing-soon"]/div')
        arr = []
        for i in list:
            dic = {}
            id = i.xpath('./a/@href')[0]
            target = '/subject/'
            index = id.rindex(target) + len(target)
            s = id[index:-1]
            dic['id'] = s

            img = i.xpath('./a/img/@src')[0]
            dic['img'] = img

            title = i.xpath('./div/h3/a/text()')[0]
            dic['title'] = title
            ls = i.xpath('./div/ul/li//text()')
            dic['up_date'] = ls[0]
            dic['category'] = ls[1]
            dic['region'] = ls[2]
            dic['see'] = ls[3]
            arr.append(dic)
        obj = {
            'subject': arr,
            'title': '即将上映',
            'city': city
        }
        return self.json_success(obj)

    # json统一返回
    def json_success(self, data, msg='请求成功'):
        obj = {
            'code': 200,
            'msg': msg,
            'data': data,
            'coderYJ': '简书关注coderYJ, 技术交流QQ群 277030213'
        }
        js = json.dumps(obj)
        return js

    def json_error(self, msg='获取失败'):
        obj = {
            'code': 400,
            'msg': msg,
            'data': None,
            'coderYJ': '简书关注coderYJ, 技术交流QQ群 277030213'
        }
        js = json.dumps(obj)
        return js
    # 详情
    def detail(self, id):
        if id == None:
            return self.json_error('id不能为空')

        self.url = 'https://movie.douban.com/subject/' + id + '/?from=playing_poster'
        result = self.getHtml()
        dic = {}
        # 标题
        title = result.xpath('//div[@id="content"]/h1/span/text()')
        title = ''.join(title)
        dic['title'] = title

        # 图片
        img = result.xpath('//div[contains(@class, "subject")]/div[@id="mainpic"]//img/@src')[0]
        dic['img'] = img

        # 导演
        director = result.xpath('//div[@id="info"]/span/span[@class="attrs"]/a[@rel="v:directedBy"]/text()')[0]
        dic['director'] = director
        # 编剧
        # director = result.xpath('//div[@id="info"]/span[@class="actor"]/span[@class="attrs"]//text()')[0]

        # 主演
        starring = result.xpath('//div[@id="info"]/span[@class="actor"]//a[@rel="v:starring"]//text()')
        dic['starring'] = starring

        genre = result.xpath('//div[@id="info"]/span[@property="v:genre"]/text()')
        dic['genre'] = genre

        up_date = result.xpath('//div[@id="info"]/span[@property="v:initialReleaseDate"]/text()')
        dic['up_date'] = up_date

        runtime = result.xpath('//div[@id="info"]/span[@property="v:runtime"]/text()')[0]
        dic['runtime'] = runtime
        # 评分
        average = result.xpath('//div[@id="interest_sectl"]//strong[@property="v:average"]/text()')[0]
        dic['average'] = average
        # 多少人评论
        votes = result.xpath('//div[@id="interest_sectl"]//span[@property="v:votes"]/text()')[0]
        dic['votes'] = votes
        # 描述
        summary = result.xpath('//div[@id="link-report"]//span/text()')[0].strip()
        dic['summary'] = summary

        return self.json_success(dic)

    # 评论
    def reviews(self, id = '', page = 0):
        if id == None or id == '':
            return self.json_error('id不能为空')
        try:
            page = int(page)
        except:
            page = 0
        if page < 0:
            page = 0
        self.url = 'https://movie.douban.com/subject/'+ id +'/reviews?start=' + str(page*20)
        result = self.getHtml()

        # 总数
        count = result.xpath('//h1/text()')
        count = '.'.join(count)
        count = re.findall(r'\d+', count)
        count = '.'.join(count)
        count = int(count)

        arr = []
        list = result.xpath('//div[contains(@class, "review-list")]/div')
        for i in list:
            dic = {}
            avator = i.xpath('./div//a[@class="avator"]/img/@src')[0]
            dic['avator'] = avator

            name = i.xpath('./div//a[@class="name"]/text()')[0]
            dic['name'] = name

            date = i.xpath('./div//span[@class="main-meta"]/text()')[0]
            dic['date'] = date

            star = i.xpath('./div//span[contains(@class, "main-title-rating")]/@title')
            if len(star) > 0:
                star = star[0]
            else:
                star = ''
            dic['star'] = star
            # 评论内容
            content = i.xpath('./div//div[@class="short-content"]/text()')
            content = ''.join(content).replace("()", '').strip()
            dic['content'] = content
            arr.append(dic)
            # print(content)
        obj = {
            'total': count,
            'page': page,
            'limit': 20,
            'subject': arr
        }
        return self.json_success(obj)

    # 获取从字符串中获取数字
    def getId(self, href):
        target = '/subject/'
        index = href.rindex(target) + len(target)
        s = href[index:-1]
        return s

    # top250
    def top250(self, page=0):
        try:
            page = int(page)
        except:
            page = 0
        if page < 0:
            page = 0

        self.url = 'https://movie.douban.com/top250?start=' + str(page*25) + '&filter='
        result = self.getHtml()
        list = result.xpath('//ol[@class="grid_view"]/li/div')
        arr = []
        for i in list:
            dic = {}
            arr.append(dic)
            href = i.xpath('./div[@class="pic"]//a/@href')[0]
            s = self.getId(href)
            dic['id'] = s
            img = i.xpath('./div[@class="pic"]//img/@src')[0]
            dic['img'] = img

            title = i.xpath('./div/div[@class="hd"]/a/span/text()')
            t_arr = []
            for k in title:
                k = k.replace("\xa0/\xa0", '')
                t_arr.append(k)
            dic['title'] = t_arr

            star = i.xpath('./div/div[@class="bd"]//div[@class="star"]/span/text()')
            dic['average'] = star[0]
            dic['evaluation'] = star[1]

            descript = i.xpath('./div/div[@class="bd"]/p[@class]//text()')
            # s = ''.join(descript).replace(" ", '').replace('\n', "")
            des_arr = []
            for j in descript:
                s = j.replace('\n', '').replace('\xa0', '').strip()
                if len(s) == 0:
                    continue
                des_arr.append(s)
            for i, w in enumerate(des_arr):
                if i == 0:
                    try:
                        a1 = w.index('导演: ') + 4
                        a2 = w.index('主')
                        s = w[a1:a2]
                        dic['director'] = s
                    except:
                        pass
                elif i == 1:
                    dic['plot'] = w
                elif i == 2:
                    dic['quote'] = w
        obj = {
            'total': 250,
            'page': page,
            'limit': 25,
            'subject': arr
        }
        return self.json_success(obj)

    # search
    def search(self, q='', page=0):
        try:
            page = int(page)
        except:
            page = 0
        if page < 0:
            page = 0
        if q == None or q == '':
            return self.json_error("请输入关键字")

        # https://api.apiopen.top/getJoke?page=1&count=2&type=video
        self.url = 'https://m.douban.com/j/search/?q='+ q +'&t=movie&p=' + str(page)
        headers = {
            "User-Agent": 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
        }
        r = requests.get(self.url, headers=headers)
        data = json.loads(r.text)
        count = data['count']
        # html数据
        h = data['html']

        limit = data['limit']
        # 转换 xpath html
        et = html.etree
        result = et.HTML(h)
        list = result.xpath('//li')
        arr = []
        for i in list:
            dic = {}
            id = i.xpath('./a/@href')[0]
            s = self.getId(id)
            dic['id'] = s
            img = i.xpath('./a/img/@src')[0]
            dic['img'] = img
            title = i.xpath('./a//span[@class="subject-title"]/text()')[0]
            dic['title'] = title
            # star
            star = i.xpath('./a//p/span/text()')[0]
            dic['star'] = star
            arr.append(dic)

        obj = {
            'count': count,
            'limit': limit,
            'subject': arr
        }
        return self.json_success(obj)
if __name__ == '__main__':
    d = Douban()
    d.nowPlaying()