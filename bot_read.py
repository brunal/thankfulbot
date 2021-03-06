#!/usr/bin/python

# with the help of http://pythonforengineers.com/

import praw
import re
from config_bot import *

r = praw.Reddit(user_agent = 'bot 0.1 by /u/poupipoupipoupipou')
r.login( os.environ['REDDIT_USERNAME'],  os.environ['REDDIT_PASS'])


key_word = 'thankfulbot'
s = ''
authorList = []
first = 'true'

with open("posts_replied_to.txt", "r") as f:
        posts_replied_to = f.read()
        posts_replied_to = posts_replied_to.split("\n")
        posts_replied_to = filter(None, posts_replied_to)
	
def bot_action(c, verbose=True, respond=True):
	global first
	global s
	global authorList
	
	submission = r.get_submission(url=c.link_url)
	if submission.id not in posts_replied_to:
		authorCom = str(c.author)
		authorPost = str(c.link_author)
		flat_comments = praw.helpers.flatten_tree(submission.comments)
		for comment in flat_comments:	
			if comment.author.name != authorCom and comment.author.name != authorPost:
				if comment.author.name not in authorList:
					if first == 'true':
						s += '/u/'+str(comment.author.name)
					else:
						s += ', /u/' + str(comment.author.name)
					authorList.append(comment.author.name)
					first = 'false'
		response = ' I\' m a lazy bot. Thank you ' + s
		if len(authorList) > 1:
			response += ' for your kind answers !'
		else:
			response += ' for your kind answer !'
		print(response)
		c.reply(response)
		posts_replied_to.append(submission.id)
	
		with open("posts_replied_to.txt", "w") as f:
			for post_id in posts_replied_to:
				f.write(post_id + "\n")

for c in praw.helpers.comment_stream(r, 'all'):
	if re.search(key_word, c.body, re.IGNORECASE):
		print(vars(c))
		bot_action(c)