### splash的使用
1.安装docker

2.启动docker

3.拉取镜像(pull the image) 
> docker pull scrapinghub/splash

4.用docker运行scrapinghub/splash服务：
> docker run -p 8050:8050 scrapinghub/splash

5.配置文件
```
1.添加splash服务器地址:
SPLASH_URL = 'http://127.0.0.1:8050'
(api提供了类似http://127.0.0.1:8050/render.html?url=http://www.baidu.com的请求)

2.将splash middleware添加到DOWNLOADER_MIDDLEWARE中
DOWNLOADER_MIDDLEWARES = {
   'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}

3.Enable SplashDeduplicateArgsMiddleware
SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}

4.Set a custom DUPEFILTER_CLASS
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'

5.a custom cache storage backend
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'
```

参考链接:
http://scrapy-cookbook.readthedocs.io/zh_CN/latest/scrapy-12.html
https://www.cnblogs.com/shaosks/p/6950358.html


