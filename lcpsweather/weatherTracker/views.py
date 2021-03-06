from django.shortcuts import render
import tweepy
from weatherTracker.credentials import creds, gmail_pass
import smtplib
import time
from datetime import datetime
import requests

# Create your views here.
def weather(request):
    def weather_getter():
        x = requests.get('http://api.openweathermap.org/data/2.5/weather?q=Ashburn&appid=1b22987782bbf4121610cdb4b60b3faa')

        weatherjson = x.json()
        print(weatherjson)

        wind = weatherjson['wind']
        coords = weatherjson['coord']
        looks = weatherjson['weather'][0]
        numbers = weatherjson['main']

        main = looks['main']
        desc = looks['description']
        icon = looks['icon']

        temp = numbers['temp']
        feels_like = numbers['feels_like']
        mint = numbers['temp_min']
        maxt = numbers['temp_max']
        pressure = numbers['pressure']
        humidity = numbers['humidity']

        windspeed = wind['speed']
        winddirection = wind['deg']
        windgust = "NEED TO FIX" # wind['gust']

        temp = int(temp)
        temp = round(temp - 273.15)
        humidity = str(humidity) + "%"

        city = weatherjson['name']

        if "rain" in desc:
            icon = 'f008'
        elif "cloud" in desc:
            icon = 'f002'
        elif "storm" in desc:
            icon = 'f010'
        elif "wind" in desc:
            icon = 'f085'
        elif "fog" in desc:
            icon = 'f003'
        elif "clear" in desc or "Clear" in desc:
            icon = 'f00d'
        
        temp = round(((temp * 9) / 5) + 32)

        return ([main, desc, temp, feels_like, mint, maxt, pressure, humidity, windspeed, winddirection, windgust, city, icon])

    weatherinfo = weather_getter()

    context = {"main": weatherinfo[0], "desc": weatherinfo[1], "temp": weatherinfo[2], "tempfeel": weatherinfo[3], "mint": weatherinfo[4], "maxt": weatherinfo[5], "pressure": weatherinfo[6], "humidity": weatherinfo[7], "windspeed": weatherinfo[8], "wind_direction": weatherinfo[9], "wind_gust": weatherinfo[10], "city": weatherinfo[11], "icon": weatherinfo[12]}

    return render(request, "twitterTracker.html", context)

def tweets(request):
    """auth = tweepy.OAuthHandler(creds["consumer_key"], creds["consumer_secret"])
    auth.set_access_token(creds["access_token"], creds["acess_token_secret"])
    api = tweepy.API(auth, wait_on_rate_limit=True)

    #ACL_tweets = api.user_timeline(screen_name = "LCPS_Academies", count = 10, exclude_replies = True)
    LCPS_tweets = api.user_timeline(screen_name = "LCPSOfficial", count = 10, exclude_replies = True)

    acl_tweets = []

    def recent_getter():
        with open("weatherTracker/detected_tweets.txt", "r") as f:
            lines = f.read()
            lines = lines.split("https")
            lines = lines[0] + " https" + lines[1]
        return lines

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
        alr_det_tweets = []

        temp = loudoun_tweet_infos


        for para in loudoun_tweet_infos:
            id = para[1]
            para = para[0]
            for word in keywords:
                if word in para:
                    try:
                        tweetstatus = api.get_status(id, tweet_mode = "extended")
                        detected_tweets.append(tweetstatus.full_text)
                    except tweepy.error.RateLimitError:
                        return [None, recent_getter()]
                else:
                    try:
                        tweetstatus = api.get_status(id, tweet_mode = "extended")
                        alr_det_tweets.append(tweetstatus.full_text)
                    except tweepy.error.RateLimitError:
                        return [None, recent_getter()]

        try:
            most_recent = detected_tweets[0]
        except:
            return [None, recent_getter()]

        with open("weatherTracker/detected_tweets.txt", "r") as f:
            tweets = f.read()

        if most_recent in tweets:
            new_detected_tweet = None
            id = loudoun_tweet_infos[0][1]
            status = api.get_status(id, tweet_mode = "extended")
            recent_tweet = status.full_text
        elif most_recent not in tweets:
            new_detected_tweet = True
            id = loudoun_tweet_infos[0][1]
            status = api.get_status(id, tweet_mode = "extended")
            new_detected_tweet = most_recent
        
        with open("weatherTracker/detected_tweets.txt", "a") as f:
                with open("weatherTracker/detected_tweets.txt", "w") as f:
                        for para in alr_det_tweets:
                            f.write(para)

        return [new_detected_tweet, status.full_text]

    def emailer(tweet, recent_tweet):
        if tweet != None:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.ehlo()

            server.login(gmail_pass['mail'], gmail_pass['pass'])

            subject = 'AVY BYARD UPDATE'
            body = recent_tweet

            msg = f"Subject: {subject}\n\n{body}"

            sender = "avyukthnilajagi@gmail.com"
            recipients = ["kanussh@gmail.com", "vchitturi9@gmail.com", "avyukthnilajagi@gmail.com", "dhruv.admala@gmail.com", "vikaskancharla05@gmail.com"]
            for i in range(len(recipients)):
                server.sendmail(sender, recipients[i], msg)
            print(" == EMAIL SENT == ")

            bool_str = "\nTWEET DETECTED == {}".format(datetime.now())
            tweet_arr = [tweet, bool_str]

            return tweet_arr

        elif tweet == None:
            bool_str = "\nNO NEW TWEETS DETECTED == {}".format(datetime.now())
            tweet_arr = [recent_tweet, bool_str]
            return tweet_arr

    with open("weatherTracker/tweet_to_display.txt", "w") as f:
        tweet_arr = (emailer(closure_getter()[0], closure_getter()[1]))
        recent_tweet = tweet_arr[0]
        detected_bool = tweet_arr[1]

        f.write(recent_tweet)
        f.write("\n" + detected_bool)

    with open("weatherTracker/tweet_to_display.txt") as f:
        text = f.read()
        if "NO" in text:
            text = text.split("NO")
            text[1] = "NO " + text[1]
        else:
            text = text.split("TWEET")
            text[1] = "TWEET " + text[1]
    
    context = {'file_content': text[0], 'file_content2': text[1]}"""

    context = {'file_content': "gay", 'file_content2': "gayer"}
    
    return render(request, "tweets.html", context)
