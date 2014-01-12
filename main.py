# Copyright 2012 Digital Inspiration
# http://www.labnol.org/

import os
from google.appengine.ext import webapp
# from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template

from google.appengine.api import mail

# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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
	html += "Atteding the brunch: " + brunch + " <br/>"
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

def buildEmail(name, eventHtml, addressHtml, comments):

	me = "rsvp@erinjaywedding.ca"
	you = "schuster.mb@gmail.com"
	subject = "RSVP - "+name

	html = """\
	<html>\
		<body>\
			<h2>Wedding RSVP</h2><br>\
			<h4>From: """ + name + """</h4>\
			""" + eventHtml + addressHtml + """\
			<h3>Additional Comments / Questions:</h3>"\
			<p>""" + comments + """</p>\
		</body>
	</html>"""

	mail.send_mail(sender=me,
					to=you,
					subject=subject,
					body=html)

	# msg = MIMEMultipart('alternative')
	# msg["From"] = me
	# msg["To"] = you
	# msg["Subject"] = "RSVP - "+name

	# message = MIMEText(html, 'html')
	# msg.attach(message)

	# s = smtplib.SMTP('localhost')
	# print s
	# s.sendmail(me, you, msg.as_string())
	# s.quit()

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
			return

		print self.request.arguments()

		name = self.request.get('name')

		## Event Information
		event = self.request.get('event')
		if event == "west":
			eventInfo = "<h3>Attending Event in the West</h3>"
			eventInfo = eventInfo + buildWestInfo(self.request)
		elif event == "east":
			eventInfo = "<h3>Attending Event in the East</h3>"
			eventInfo = eventInfo + buildEastInfo(self.request)
		elif event == "both":
			eventInfo = "<h3>Attending Both Events</h3>"
			eventInfo = "<h4>Information for event in the West</h4>"
			eventInfo = eventInfo + buildWestInfo(self.request)
			eventInfo = "<h4>Information for event in the East</h4>"
			eventInfo = eventInfo + buildEastInfo(self.request)
		elif event == "none":
			eventInfo = "<h3>Unable to attend either event</h3>"

		##  Address Information
		apptno = self.request.get('appt')
		street = self.request.get('street')
		city = self.request.get('city')
		province = self.request.get('province')
		postalcode = self.request.get('postalcode')

		address = ""
		if apptno:
			address = "#" + apptno + " - "

		addressInfo = "<h3>Address:</h3>"
		addressInfo = addressInfo + "<p>" + address + street + "<br/>"
		addressInfo = addressInfo + city + ", " + province + "<br/>"
		addressInfo = addressInfo + postalcode + "</p>"

		comments = self.request.get('comments')

		buildEmail(name, eventInfo, addressInfo, comments)

		path = os.path.join (os.path.dirname (__file__), 'pages/rsvp.html')
		self.response.headers ['Content-Type'] = 'text/html'
		self.response.out.write (template.render (path, {}))


# def main ():
application = webapp.WSGIApplication ([('/sendRSVP', RSVPHandler), ('/(.*)', MainHandler)], debug=True)
  # util.run_wsgi_app (application)

