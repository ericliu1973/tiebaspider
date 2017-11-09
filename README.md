## 运行环境
* python3.5 
* 该spider是 32线程 + twisetd异步机制，单机带宽下最大效率的进行抓取

##使用
* 根据item中定义的字段自行在mysql中建表
* 运行main文件就可

## 问题
* 运行时提示异常'[<twisted.python.failure.Failure OpenSSL.SSL.Error: [('SSL routines', 'SSL3_GET_SERVER_CERTIFICATE', 'certificate verify failed')]'

* 这是Twisted中的一个bug，你可以点击阅读更多关于它的信息:[点击](https://twistedmatrix.com/trac/ticket/6372)
* scrapy文档中[DOWNLOADER_CLIENTCONTEXTFACTORY](https://doc.scrapy.org/en/latest/topics/settings.html)

## 解决方案
* 你可以创建自己的ContextFactorySSL来处理
#### context.py：

    from OpenSSL import SSL
    from scrapy.core.downloader.contextfactory import ScrapyClientContextFactory


    class CustomContextFactory(ScrapyClientContextFactory):
        """
        Custom context factory that allows SSL negotiation.
        """
        def __init__(self):
            # Use SSLv23_METHOD so we can use protocol negotiation
            self.method = SSL.SSLv23_METHOD
#### settings.py
    DOWNLOADER_CLIENTCONTEXTFACTORY = 'yourproject.context.CustomContextFactory'
    
    
## show 
![](https://github.com/duolaAOA/tiebaspider/blob/master/pic.png?raw=true)

