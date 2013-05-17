#!/usr/bin/python
# -*- coding: utf-8 -*-

import wolframalpha
import webbrowser

class Wolfram:
	def __init__(self, tts, key):
		self.tts = tts
		self.key = key

	def process(self, job):
		if job.get_is_processed(): 
			return False

		if not self.key:
			self.tts.say("Please provide an API key to query the WolframAlpha database.")
			return False

		resp = self.query(job.raw(), self.key)

		self.tts.say(resp)

		# open wolfram alpha page if image
		if resp == "Your question was answered with an image.":
			self.open(False, job.raw())

		job.is_processed = True

	def query(self, phrase, key):
		client = wolframalpha.Client(key)
		res = client.query(phrase)

		# Parse response
		try: 
			if len(res.pods) == 0:
				raise StopIteration()

			for pod in res.results:
				if hasattr(pod.text, "encode"):
					return "The answer to your question is " + \
							pod.text.replace(u"°", ' degrees ').encode('ascii', 'ignore')
				else:
					break

			return "Your query was answered with an image."

		except StopIteration:
			return "No results for the query '" + phrase + ".'"

def say(self, text):
	return self.tts.say(text)

def open(self, wolfram, text):
	# remove wolfram from start of query if it is there
	if wolfram == True:
		text = text[7:]

	controller = webbrowser.get()
	wolfram_url = "http://www.wolframalpha.com/input/?i="
	url = wolfram_url + speaker.spacestoPluses(text)
	controller.open(url)
