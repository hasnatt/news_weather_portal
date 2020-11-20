from flask import Flask, render_template, url_for, request
# from flask_fontawesome import FontAwesome

import json
import os
import requests
import time
import config


app = Flask(__name__, static_url_path='/static')

newskey = config.newskey
weatherkey = config.weatherkey


def newsFeed(countryCode):
    url = "https://newsapi.org/v2/top-headlines?country="
    #concatinate country code to url
    url += countryCode
    # Define the params for the end point
    headers = {
        'Accept': 'application/json',
        'X-Api-Key': newskey,
    }
    try:
        # before = time.time() * 1000
        response = requests.request("GET", url, headers=headers)
        # after = time.time() * 1000
        # print("news time difference ", after - before)
    except Exception:
        return "Error: request failed"
    #load body in json format
    body = json.loads(response.text)
    #gathering articles from the api
    articles = body["articles"]
    # print(response.text)
    return articles

def weatherFeed(location):
    # Open openweathermap endpoint
    url = "http://api.openweathermap.org/data/2.5/weather"
    # Define the params
    params = {
        # q is the locatiion input in the endpoint
        # location is the variable being passed through the front end
        'q': location,
        'APPID': weatherkey,
        'units':'metric'
    }
    try:
        # before = time.time() * 1000
        #GET request data from api with the given params
        response = requests.request("GET", url, params=params)
        # after = time.time() * 1000
        # print("weather time difference ", after - before)
    except Exception:
        return "Error: request failed"
    #Load the json response
    body = json.loads(response.text)
    print(response.text)
    return body

def timeDifference(published):
        url = "http://127.0.0.1:8000/timeDiff/"
        # take in date value from NewsAPI as parameter for dateAPI calculations
        # published is the string value fed to the API
        url+= published
        #GET response from timeDiffAPI
        response = requests.request("GET", url)
        #load calculations made in API stored in body
        body = json.loads(response.text)
        return body

@app.route('/', methods = ['GET','POST'])
def home():
    # Set to New york when page loads
    if request.method == 'POST':
        location = request.form.get('location')
    else:
        #New york is default location
        location = 'New York'
    #Gather the location data from
    weather = weatherFeed(location)
    countryCode = weather["sys"]["country"]
    articles = newsFeed(countryCode)
    #return Published at the time difference via timeDiffAPI instead
    #of the datetime object string
    for article in articles:
        published = article["publishedAt"]
        i = timeDifference(published)
        i = i["difference"]["hours"]
        article["publishedAt"] = round(i,2)

    return render_template('home.html', articles=articles, weather = weather)


if __name__ == '__main__':
        app.run(debug=True)
