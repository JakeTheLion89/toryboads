import tornado.ioloop
import tornado.web
import tornado.httpclient
import tornado.escape

class MainHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        http = tornado.httpclient.AsyncHTTPClient()
        http.fetch("https://xkcd.com/614/info.0.json",
                   callback=self.on_response)

    def on_response(self, response):
        if response.error: raise tornado.web.HTTPError(500)
        json = tornado.escape.json_decode(response.body)
        self.write(json)
        self.finish()

class TestHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self,url_param):
        http = tornado.httpclient.AsyncHTTPClient()
        xkcd_url = "https://xkcd.com/" + url_param + "/info.0.json"
        print(xkcd_url)
        http.fetch(xkcd_url,callback=self.on_response)

    def on_response(self,response):
        if response.error: raise tornado.web.HTTPError(404)
        json = tornado.escape.json_decode(response.body)
        json['myAttribute'] = "THIS IS MY BLAG"
        self.write(json)
        self.finish()

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/search/([^/]+)",TestHandler)
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
