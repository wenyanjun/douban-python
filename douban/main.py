'''
@author <coderYJ>
@since <1.0.0>
@QQ群 277030213
@GitHub https://github.com/wenyanjun/douban-python
'''
from flask import Flask, request
import Douban

app = Flask(__name__)
douban = Douban.Douban()

@app.route("/")
def home():
    common('/')
    return douban.json_success(None)

# 正在上映
@app.route('/nowplaying', methods=['GET'])
def nowplaying():
    common('nowplaying')
    city = request.args.get('city')
    data = douban.nowPlaying(city)
    return data

# 即将上映
@app.route('/upcoming', methods=['GET'])
def upcoming():
    common('upcoming')
    city = request.args.get('city')
    data = douban.upcoming(city)
    return data

# 电影详情
@app.route("/detail", methods=['GET'])
def detail():
    common('detail')
    id = request.args.get('id')
    if id == None:
        return douban.json_error('id不能为空')
    data = douban.detail(id)
    return data

# 电影评论
@app.route("/reviews", methods=['GET'])
def reviews():
    common('reviews')
    id = request.args.get('id')
    page = request.args.get('page')
    data = douban.reviews(id, page)
    return data

# top250
@app.route('/top250', methods=['GET'])
def top250():
    common('top250')
    page = request.args.get('page')
    data = douban.top250(page)
    return data

# search
@app.route('/search', methods=['GET'])
def search():
    common('search')
    page = request.args.get('page')
    q = request.args.get('q')
    data = douban.search(q, page)
    return data
# common
def common(method):
    ip = request.remote_addr
    print(ip, method)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)