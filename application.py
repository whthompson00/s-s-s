import os
import sys

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
import datetime
import schedule
import time

from helpers import apology

from GLICKO import newRD, newRating, estimated

from urllib.request import urlopen
from bs4 import BeautifulSoup

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True




# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///records.db")


@app.route("/")
def index():
    return render_template("index.html")


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


def updateRating():
    # choose all the games which have not been used to update ratings yet
    games = db.execute("SELECT * FROM records WHERE inserted = 0")
    # iterate through all the games
    for game in games:
        # select the teams playing in the game
        team1 = db.execute("SELECT * FROM teams WHERE Abrv = :Abrv", Abrv = game["Team1"])
        team2 = db.execute("SELECT * FROM teams WHERE Abrv = :Abrv", Abrv = game["Team2"])
        # in case of a d3 school not in the database
        if not team1:
            r1 = 800
            RD1 = 500
        else:
            # get the first team's rating and RD
            r1 = int(team1[0]["rating"])
            RD1 = int(team1[0]["RD"])
        # in case second team is d3 and not in database
        if not team2:
            r2 = 800
            RD2 = 500
        else:
            # get the first team's rating and RD
            r2 = int(team2[0]["rating"])
            RD2 = int(team2[0]["RD"])
        # based off the scores, calculate which team won, as well as the margin of victory
        if game["Score1"] > game["Score2"]:
            outcome1 = 1
            outcome2 = 0
            MoV = int(game["Score1"] - game["Score2"])
        else:
            outcome1 = 0
            outcome2 = 1
            MoV = game["Score2"] - game["Score1"]
        # call the newRating function in GLICKO.py to get the new rating of both teams
        total = game["Score1"] - game["Score2"]
        newR1 = newRating(r1, RD1, r2, RD2, outcome1, MoV, total)
        newR2 = newRating(r2, RD2, r1, RD1, outcome2, MoV, total)
        # call the newRD function in GLICKO.py to get the new RD of both teams
        newRD1 = newRD(r1, RD1, r2, RD2)
        newRD2 = newRD(r2, RD2, r1, RD1)
        # check again to make sure team1 and team2 are in the database of teams (ie not d3)
        if team1:
            # update the rating of team1 in the database
            db.execute("UPDATE Teams SET rating = :newR1 WHERE Abrv = :Abrv", newR1=int(newR1), Abrv = game["Team1"])
            # update the RD of team1 in the database
            db.execute("UPDATE Teams SET RD = :newRD1 WHERE Abrv = :Abrv", newRD1=int(newRD1), Abrv = game["Team1"])
        if team2:
            # same as above but with team 2
            db.execute("UPDATE Teams SET rating = :newR2 WHERE Abrv = :Abrv", newR2=int(newR2), Abrv = game["Team2"])
            db.execute("UPDATE Teams SET RD = :newRD2 WHERE Abrv = :Abrv", newRD2=int(newRD2), Abrv = game["Team2"])
        # change inserted to 1 so computer knows the game has updated rating
        db.execute("UPDATE records SET inserted = 1 WHERE Team1 = :Abrv1 AND Team2 = :Abrv2 AND inserted = 0", Abrv1 = game["Team1"], Abrv2 = game["Team2"])

def loadGames(initial):
    # if doing the initial load, load all the games from the beginning to the end of the season
    # note only the game results will only show up if the game has been played
    if initial is 1:
        start = datetime.datetime.strptime("06-11-2018", "%d-%m-%Y")
        end = datetime.datetime.strptime("25-03-2019", "%d-%m-%Y")
        # generates a list of dates from the beginning of season to end of the season
        date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]
    else:
        # just get yesterday's date for the daily update
        date_generated = []
        yesterday = datetime.datetime.today() - datetime.timedelta(1)
        date_generated.append(yesterday)
    # for every date generated in the list
    for date1 in date_generated:
        # reformat date to match form in ESPN's URL
        date2 = date1.strftime("%Y%m%d")
        # The ESPN webpage with all the college basketball results of a specific day
        quote_page = 'http://www.espn.com/mens-college-basketball/schedule/_/date/'+date2+'/group/50'
        # open the webpage for scraping
        page = urlopen(quote_page)
        # scrape the html from the URL with BeautifulSoup
        soup = BeautifulSoup(page, 'html.parser')
        # get all the games from the webpage, using the fact that the 'name' of the element is '&lpos=mens-college-basketball:schedule:score'
        for game in soup.find_all(attrs={'name': '&lpos=mens-college-basketball:schedule:score'}):
            # format the text of the game
            game = game.text
            # split the game into a list of elements
            # order of list is (team1, team2, score1, score2)
            outcome = game.split()
            # check to make sure the game was not cancalled or postponed
            if (len(outcome) is not 1):
                # remove an extraneous comma
                outcome[1] = outcome[1].replace(',' , '')
                # put the outcome into the records database in order as specified in db of team1, score1, team2, score2
                db.execute("INSERT INTO records (team1, team2, score1, score2) VALUES(:team1, :team2, :score1, :score2)",
                              team1=outcome[0], team2=outcome[2], score1=outcome[1], score2=outcome[3])


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

def loadTeams():
    # scrape ESPN to load all the college teams into the database
    quote_page = 'http://www.espn.com/mens-college-basketball/teams'
    # open the webpage to scrape
    page = urlopen(quote_page)
    # parse the HTML using BeautifulSoup
    soup = BeautifulSoup(page, 'html.parser')
    teamId = 1
    # for every team name found on the page (ie element with class 'clr-gray-01 di h5'), add the team to the database
    for name in soup.find_all('h2', attrs={'class': 'clr-gray-01 di h5'}):
        db.execute("INSERT INTO Teams (TeamName, teamId) VALUES(:name, :teamId)", name=name.text, teamId=teamId)
        teamId += 1

def main ():
    #loadTeams()
    loadGames(1)
    updateRating()

# https://pypi.org/project/schedule/
# load all the previous day's games into records at 6 am
# update the ratings based on those results
schedule.every().day.at("6:00").do(loadGames, 0)
schedule.every().day.at("6:01").do(updateRating)

@app.route("/rankings", methods=["GET"])
def rankings():

    Teams = db.execute("SELECT * FROM Teams")
    # sort the teams in terms of their ratings with mergeSort
    sortedTeams = mergeSort(Teams)

    return render_template("rankings.html", Teams=sortedTeams)

@app.route("/headtohead", methods=["GET", "POST"] )
def headtohead():

    if request.method == "POST":
        # make sure the user entered a team1
        if not request.form.get("team1"):
            return apology("You must enter Your Team!")
        # make sure the user entered a team2
        elif not request.form.get("team2"):
            return apology("You must enter Your Opponent!")

        # select the two teams based on the names entered
        team1 = db.execute("SELECT * FROM Teams WHERE TeamName = :TeamName", TeamName=request.form.get("team1"))
        team2 = db.execute("SELECT * FROM Teams WHERE TeamName = :TeamName", TeamName=request.form.get("team2"))

        # check to make sure the teams exist
        if not team1:
            # if the team does not exist, see if the user entered an abreviation for a team (ie UVa)
            team1 = db.execute("SELECT * FROM Teams WHERE Abrv = :Abrv", Abrv=(request.form.get("team1")).upper())
            # otherwise, return an error
            if not team1:
                return apology("Your Team does not Exist!")
        # same as above
        if not team2:
            team2 = db.execute("SELECT * FROM Teams WHERE Abrv = :Abrv", Abrv=(request.form.get("team2")).upper())
            if not team2:
                return apology("Your Opponent does not Exist!")
        # smooth results
        team1Rating = ((team1[0]["rating"] / 1500) ** (1/3)) * 1500
        team2Rating = ((team2[0]["rating"] / 1500) ** (1/3)) * 1500
        # call the estimated function from GLICKO.py to see the estimated win probabilities
        chances1 = ((estimated(team1Rating, team2Rating, team2[0]["RD"])) * 100)
        chances2 = 100 - chances1
        # find the other teams win percentage
        # return the template with the win probabilities
        return render_template("forecast.html", team1=team1[0]["TeamName"], team2=team2[0]["TeamName"], chances1=chances1, chances2=chances2)

    return render_template("headtohead.html")

# mergeSort
# ammended from https://pythonandr.com/2015/07/05/the-merge-sort-python-code/
def mergeSort(teams):
    if len(teams) is 1 or 0:
        return teams
    else:
        middle = int(len(teams) / 2)
        # split the list into two until the list cannot be split more -- use recursion
        front = mergeSort(teams[:middle])
        back = mergeSort(teams[middle:])
        # merge all the split pieces back together
        return merge(front, back)

def merge(front, back):
    final = []
    f = 0
    b = 0
    # iterate through the two lists
    while len(front) > f and len(back) > b:
        # check whether the current element of front is greater than or less than current element of back
        if front[f]["rating"] > back[b]["rating"]:
            # append the element from front if front is larger
            final.append(front[f])
            # move to next element in front
            f += 1
        else:
            # append the element from back if back is larger
            final.append(back[b])
            # move to next element in back
            b += 1
    # if all the front has been added to list, add the rest of back, which is already ordered
    if len(front) is f:
        while len(back) > b:
            final.append(back[b])
            b += 1
     # if all the back has been added to list, add the rest of front, which is already ordered
    else:
        while len(front) > f:
            final.append(front[f])
            f += 1
    # return the merged list
    return final

if __name__ == "__main__":
    main()