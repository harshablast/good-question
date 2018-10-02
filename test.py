from textblob import TextBlob
import numpy as np
from rake_nltk import Rake




def sentiment(sentence):
	return TextBlob(sentence).polarity

def reply_negative():
	replies = ["We're sorry to hear that.",
				"We wish to help you with that.",
				"We're sorry for the inconvenience caused.",
				"We will definitely improve."]

	return replies[np.random.randint(0,3)]+"Tell us something more about it."

def reply_positive():
	replies = ["Great!",
				"That is good to hear!",
				"We are glad to help you.",
				"Amazing!"]
	return replies[np.random.randint(0,3)]

def get_keywords(sentence):
		r = Rake()
		r.extract_keywords_from_text(sentence)
		return r.get_ranked_phrases()

def show_analysis(d):

	for key,value in d.items():
		print(key, ":", value)
import flask
def filter_questions(sentence):	
	if TextBlob(sentence).tags[0][1] == 'WRB' or TextBlob(sentence).tags[0][1] == 'WP':
		print('SHITBOT: I don\'t understand. Please answer as asked.')
		return 1

collected_data = {}

questions = ["What do you feel about the teaching?",
			"Your opinion about the course content?",
			"Were we helpful during examinations?",
			"How did you find the lab work?",
			"Your opinion about the library?",
			"What do you feel about extra-curricular?"]

def converse():
	for i in questions:
		print("SHITBOT: ",i)
		ans = input(">>")
		while (filter_questions(ans)):
			print("SHITBOT: ",i)
			ans = input(">>")
			print('inside loop')

		if sentiment(ans) < 0 :

			reply = reply_negative()
			print(reply)
			additional_ans = input(">>")

			collected_data[additional_ans] = get_keywords(additional_ans)

		else :

			reply = reply_positive()
			print(reply)



converse()
print(collected_data)






