import tweepy
from credentials import creds, gmail_pass
import smtplib
import time
from datetime import datetime

auth = tweepy.OAuthHandler(creds["consumer_key"], creds["consumer_secret"])
auth.set_access_token(creds["access_token"], creds["acess_token_secret"])
api = tweepy.API(auth)

ACL_tweets = api.user_timeline(screen_name = "LCPS_Academies", count = 200, exclude_replies = True)
LCPS_tweets = api.user_timeline(screen_name = "LCPSOfficial", count = 200, exclude_replies = True)

acl_tweets = []

def closure_getter():
    loudoun_tweet_infos = []
    tweet_info = []

    keywords = ["weather", "delay", "on time", "closure", "opening", "inclement", "cancelled", "closed", "closing"]

    for tweet in LCPS_tweets:
        info = tweet.text + " SEPERATOR " + str(tweet.id)
        loudoun_tweet_infos.append(info)

    for i in range(len(loudoun_tweet_infos)):
        info = loudoun_tweet_infos[i]
        info_list = info.split(" SEPERATOR ")
        loudoun_tweet_infos[i] = info_list

    detected_tweets = []

    temp = loudoun_tweet_infos

    for para in loudoun_tweet_infos:
        id = para[1]
        para = para[0]
        for word in keywords:
            if word in para:
                tweetstatus = api.get_status(id, tweet_mode = "extended")
                detected_tweets.append(tweetstatus.full_text)

    try:
        most_recent = detected_tweets[0]
    except:
        pass

    with open("detected_tweets.txt", "r") as f:
        tweets = f.read()

    if most_recent in tweets:
        new_detected_tweet = None
        id = loudoun_tweet_infos[0][1]
        status = api.get_status(id, tweet_mode = "extended")
        recent_tweet = status.full_text
    elif most_recent not in tweets:
        new_detected_tweet = most_recent

    with open("detected_tweets.txt", "a") as f:
            with open("detected_tweets.txt", "w") as f:
                    for para in detected_tweets:
                        f.write(para)

    return (new_detected_tweet, status.full_text)

def emailer(tweet, recent_tweet):
    if tweet != None:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()

        server.login(gmail_pass['mail'], gmail_pass['pass'])

        subject = 'AVY BYARD UPDATE'
        body = tweet

        msg = f"Subject: {subject}\n\n{body}"

        sender = "avyukthnilajagi@gmail.com"
        recipients = ["kanussh@gmail.com", "vchitturi9@gmail.com", "avyukthnilajagi@gmail.com", "dhruv.admala@gmail.com"]
        for i in range(len(recipients)):
            server.sendmail(sender, recipients[i], msg)
        print(" == EMAIL SENT == ")

    elif tweet == None:
        return(recent_tweet, ("\nNO NEW TWEETS DETECTED == {}".format(datetime.now())))

with open("tweet_to_display.txt", "w") as f:
    f.write(emailer(closure_getter()[0], closure_getter()[1])[0])
    f.write("\n")
    f.write("              __________________                      ")
    f.write("\n")
    f.write(emailer(closure_getter()[0], closure_getter()[1])[1])

