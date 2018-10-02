from textblob import TextBlob
import numpy as np
from rake_nltk import Rake
from flask import request
from flask_cors import CORS
from pymongo import MongoClient
import flask

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

def filter_questions(sentence):	
	if TextBlob(sentence).tags[0][1] == 'WRB' or TextBlob(sentence).tags[0][1] == 'WP':
		print('I don\'t understand. Please answer as asked.')
		return 1

collected_data = {}	
questions = ["What do you feel about the teaching?",
			"Your opinion about the course content?",
			"Were we helpful during examinations?",
			"How did you find the lab work?",
			"Your opinion about the library?",
			"What do you feel about extra-curricular?"]

app = flask.Flask(__name__)
CORS(app)
client = MongoClient()
client = MongoClient('mongodb://localhost:27017/')
teacher_analytics = client.test_database.teacher_analytics

@app.route("/chat",methods=["POST"])
def converse():

	question = request.form.get('question')
	print(question)
	ans = input(">>")
	if filter_questions(ans):
		return flask.jsonify({'comment':'I don\'t understand. Please answer as asked.',
			'question':question})

	if sentiment(ans) < 0 :

		reply = reply_negative()
		additional_ans = input(">>")
		collected_data[additional_ans] = get_keywords(additional_ans)

	else :

		reply = reply_positive()
	data = {'teacher_id' : '123', 'reply': reply, 'sentiment': sentiment(ans), 'collective': collected_data}
	teacher_analytics.insert_one(data)

	return flask.jsonify(data)


if __name__ == '__main__':
	app.run(host='localhost',port=5000)











