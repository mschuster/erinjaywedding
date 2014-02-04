# Copyright 2012 Digital Inspiration
# http://www.labnol.org/

import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import mail

def buildWestInfo(req):
	html = "<p>"
	if req.get('west-guest'):
		guest = req.get('west-guest-name')
	else:
		guest = "none"

	html += "Guest: " + guest + "<br/>"

	if req.get('west-children'):
		children = req.get('west-children-name')
	else:
		children = "none"

	html += "Bringing Children: " + children + "<br/>"

	stay = req.get('west-stay')
	brunch = req.get('west-brunch')

	html += "Staying for " + stay + " Night(s) <br/>"
	html += "Attending the brunch: " + brunch
	html += "</p>"

	return html

def buildEastInfo(req):
	html = "<p>"
	if req.get('east-guest'):
		guest = req.get('east-guest-name')
	else:
		guest = "none"

	html += "Guest: " + guest + "<br/>"

	if req.get('east-children'):
		children = req.get('east-children-name')
	else:
		children = "none"

	html += "Bringing Children: " + children + "<br/>"
	html += "</p>"

	return html

def buildEmail(name, eventInfo, address, comments):

	me = "mschuster@erinjaywedding.ca"
	subject = "RSVP - "+name

	message = mail.EmailMessage(sender=me,
								subject=subject)

	message.to = "schuster.mb@gmail.com"
	# message.to = "guardian.angelhs@gmail.com"

	message.html = """\
	<html>
		<body>
			<h2>Wedding RSVP</h2>
			<h4>From: """ + name + """</h4>
			<h3>""" + eventInfo['attending'] + """</h3>
			<p>\
				""" + eventInfo['detail'] + """\
			</p>\
			<h3>Address: </h3>
			<p>
				""" + address['street'] + """ <br/>
				""" + address['city'] + """, """ + address['province'] + """<br/>
				""" + address['postalcode'] + """
			</p>
			<h3>Additional Comments / Questions:</h3>"
			<p>""" + comments + """</p>
		</body>
	</html>"""

	message.body = """
		Wedding RSVP

		From: """ + name + """

		Event Information: \
		""" + eventInfo['attending'] + """
		""" + eventInfo['detail'] + """

		Address:
		""" + address['street'] + """
		""" + address['city'] + """, """ + address['province'] + """
		""" + address['postalcode'] + """

		Additional Comments: \
		""" + comments + """
		"""


	message.send()


class MainHandler(webapp.RequestHandler):
	def get (self, q):

		if not q:
			q = 'story'
		# if "." not in q:
		# 	q = q + '.html'

		path = os.path.join (os.path.dirname (__file__), 'pages/' + q + '.html')
		self.response.headers ['Content-Type'] = 'text/html'
		self.response.out.write (template.render (path, {}))

class RSVPHandler(webapp.RequestHandler):

	def post (self):
		if not self.request.arguments():
			print "no arguments"
			path = os.path.join (os.path.dirname (__file__), 'pages/rsvp.html?message=error')
			self.response.headers['Content-Type'] = 'text/html'
			self.response.out.write (template.render (path, {}))
			return

		name = self.request.get('name')

		## Event Information
		event = self.request.get('event')
		eventInfo = {}
		eventInfo['attending'] = "Unable to attend either event"
		eventInfo['detail'] = ""
		if event == "west":
			eventInfo['attending'] = "Attending Celebrations in BC"
			eventInfo['detail'] = buildWestInfo(self.request)
		elif event == "east":
			eventInfo['attending'] = "Attending Lunch Celebration in Toronto"
			eventInfo['detail'] = buildEastInfo(self.request)
		elif event == "both":
			eventInfo['attending'] = "Attending Both Events"
			eventInfo['detail'] = "<h4>Information for celebrations in BC</h4>"
			eventInfo['detail'] = eventInfo['detail'] + buildWestInfo(self.request)
			eventInfo['detail'] = eventInfo['detail'] + "<h4>Information for lunch in Toronto</h4>"
			eventInfo['detail'] = eventInfo['detail'] + buildEastInfo(self.request)

		##  Address Information
		address = {}

		apptno = self.request.get('appt')
		address['street'] = self.request.get('street')
		address['city'] = self.request.get('city')
		address['province'] = self.request.get('province')
		address['postalcode'] = self.request.get('postalcode')

		if apptno:
			address['street'] = "#" + apptno + " - " + address['street']


		comments = self.request.get('comments')

		buildEmail(name, eventInfo, address, comments)

		path = os.path.join (os.path.dirname (__file__), 'pages/rsvp.html?message=sent')
		self.response.headers['Content-Type'] = 'text/html'
		self.response.out.write (template.render (path, {}))


application = webapp.WSGIApplication ([('/sendRSVP', RSVPHandler), ('/(.*)', MainHandler)], debug=True)

