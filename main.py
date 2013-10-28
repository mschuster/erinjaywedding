# Copyright 2012 Digital Inspiration
# http://www.labnol.org/

import os
from google.appengine.ext import webapp
# from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template

class MainHandler(webapp.RequestHandler):
	def get (self, q):

		if not q:
			q = 'story'
		# if "." not in q:
		# 	q = q + '.html'

		path = os.path.join (os.path.dirname (__file__), 'pages/' + q + '.html')
		self.response.headers ['Content-Type'] = 'text/html'
		self.response.out.write (template.render (path, {}))

# def main ():
application = webapp.WSGIApplication ([('/(.*)', MainHandler)], debug=True)
  # util.run_wsgi_app (application)

# if __name__ == '__main__':
#   main ()

# # Copyright 2012 Digital Inspiration
# # http://www.labnol.org/

# import os
# import webapp2
# # from webapp2 import util
# # from webapp2 import template
# # from google.appengine.ext import webapp
# # from google.appengine.ext.webapp import util
# from google.appengine.ext.webapp import template

# class MainHandler(webapp2.RequestHandler):
#   def get (self, q):
#     if q is None:
#       q = 'index'

#     path = os.path.join (os.path.dirname (__file__), q + '.html')
#     self.response.headers ['Content-Type'] = 'text/html'
#     self.response.write (path)


# # def main ():
# application = webapp2.WSGIApplication ([('/(.*)', MainHandler)], debug=True)
#   # return application
#   # util.run_wsgi_app (application)

# # if __name__ == '__main__':
# #   application = main ()