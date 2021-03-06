import praw
import re
import requests
import datetime
import logging

# Logging Logic
log_format = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename = 'errors.log', level=logging.DEBUG, format=log_format)
logging.debug('Test message')
logger = logging.getLogger()

# Validates credentials with api
redditInfo = praw.Reddit(
                            client_id = 'client_id',
                            client_secret = 'client_secret',
                            username = 'username',
                            user_agent = 'user_agent')

# GETS information from a subreddit
subreddit = redditInfo.subreddit('subreddit')
post_date = ""


# Regex to find match info in pre match thread
matchFinder = re.compile(r'Pre Match')
dateFinder = re.compile(r'Date:...........')
kickOffFinder = re.compile(r'Kick off.........', re.IGNORECASE)
timeFinder = re.compile(r'\d\d')

# Slack API Data 
slack_url = "slack_url"
payload = {"text": "No Match Today"}
payloadSTR = ""

# Running the test for time converter from GMT to CST (subtract 5 hours from GST to get the CST) need to add an argument to function so that it can take the text in the post and find the necessary info
def time_converter(subreddit_txt): 
    #testT = redditInfo.submission(id='cue12g')
    dateNum = str(kickOffFinder.findall(subreddit_txt.selftext))
    GSTTime = timeFinder.findall(dateNum)
    CSTTime = int(GSTTime[0]) - 6
    logger.critical(GSTTime)
    logger.critical(GSTTime[0])
    logger.critical(int(GSTTime[0]) - 6)
    logger.critical(CSTTime)
    return str(CSTTime) + ':' + str(GSTTime[1]) 


"""
def time_getter(subreddit_txt):
	dateNum = str(kickOffFinder.findall(subreddit_txt.selftext))
    	GSTTime = timeFinder.findall(dateNum)
	logger.debug(str(GSTTime))
"""


# Loop that runs through new threads and runs Regex to find prematch thread
for insta in subreddit.new():
	if insta.stickied == True:
	    if matchFinder.findall(insta.title) == []:
		continue
	    else:
		# this calls the text found on the submission what we want to look for is kick off time
		# refrence the screenshot to get information of prematch text; screenshot can be found in the resources directory
		# insta.title + str(.findall(insta.selftext))
		payloadSTR = insta.title + " " + str(dateFinder.findall(insta.selftext)) + " " + time_converter(insta)
		#str(kickOffFinder.findall(insta.selftext)) 
		#Post date will be used to verify if the game has already been played so as not to send a message because the pre match thread is still hainging aroun 
		post_date = str(dateFinder.findall(insta.selftext)) 
		logger.info(payloadSTR)
		# print(insta.title)
		# print(str(kickOffFinder.findall(insta.selftext)))

payload["text"] = payloadSTR


def slack_message(url, payload):
    try:
	requests.post(url = url, json = payload)
    except Exception as err:
	logger.info(str(err))


slack_message(slack_url, payload)
# if statement needs to check datetime vs the date finder and send the message if on or before the current date

