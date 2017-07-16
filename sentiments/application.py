from flask import Flask, redirect, render_template, request, url_for

import helpers
import os
import sys

from analyzer import Analyzer

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():

    # validate screen_name
    screen_name = request.args.get("screen_name", "")
    if not screen_name:
        return redirect(url_for("index"))

    # get screen_name's tweets
    tweets = helpers.get_user_timeline(screen_name)
    
    if helpers.get_user_timeline(screen_name) == None:
        return redirect(url_for("index"))
        
    else:
        positives = os.path.join(sys.path[0], "positive-words.txt")
        negatives = os.path.join(sys.path[0], "negative-words.txt")
        
        # instantiate analyzer
        analyzer = Analyzer(positives, negatives)
        
        positive = 0
        negative = 0
        neutral = 0
        
        
        # check for the last 200 tweets if they're positive, negative or neutral
        for i in range(200):
            # analyze word
            score = analyzer.analyze(tweets[i])
            
            if score > 0.0:
                positive += 1
            elif score < 0.0:
                negative += 1
            else:
                neutral += 1


    # generate chart
    chart = helpers.chart(positive, negative, neutral)

    # render results
    return render_template("search.html", chart=chart, screen_name=screen_name)
