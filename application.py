import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash
from passlib.apps import custom_app_context as pwd_context

from helpers import apology, login_required, lookup, usd

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


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    # get the list of the user's stocks
    stocks = db.execute("SELECT * FROM portfolio WHERE id=:id", id=session["user_id"])
    # calculate the total value of the stocks
    totalValue = 0
    # iterate through the stocks
    for i in range(len(stocks)):
        tickerSymbol = stocks[i]["tickerSymbol"]
        quote = lookup(tickerSymbol)
        currentPrice = quote["price"]
        value = currentPrice * stocks[i]["quantity"]
        totalValue = value + totalValue
        # update for the current price of the stock
        db.execute("UPDATE portfolio set currentPrice=:currentPrice WHERE id=:id AND tickerSymbol=:tickerSymbol",
                   currentPrice=usd(currentPrice), id=session["user_id"], tickerSymbol=tickerSymbol)
        # update for the new value of the stock
        db.execute("UPDATE portfolio set value=:value WHERE id=:id AND tickerSymbol=:tickerSymbol",
                   value=usd(value), id=session["user_id"], tickerSymbol=tickerSymbol)
    # get the updated list of stocks
    stocks = db.execute("SELECT * FROM portfolio WHERE id=:id", id=session["user_id"])
    user = db.execute("SELECT * FROM users WHERE id=:id", id=session["user_id"])
    # the amount of user's cash
    cash = int(user[0]["cash"])
    # the total value of the account
    totalValue = totalValue + cash
    # display the table of the portfolio and send cash and total value
    return render_template("index.html", stocks=stocks, cash=usd(cash), total=usd(totalValue))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "POST":
        # get the symbol the user entered
        symbol = request.form.get("symbol")
        quote = lookup(symbol)
        # check to make sure the user entered an int for the number of shares
        if not request.form.get("shares").isdigit():
            return apology("Must enter a postive int", 400)
        shares = int(request.form.get("shares"))
        # if the symbol was not a real ticker symbol return an error
        if not quote:
            return apology("not a valid symbol", 400)
        # make sure shares is a non negetive number
        if not (int(shares) > 0):
            return apology("you must input a non-negetive number", 400)
        # get the cash of the user
        money = db.execute("SELECT cash FROM users WHERE id=:id", id=session["user_id"])
        purchasePrice = quote["price"]
        value = purchasePrice * shares
        # ensure the user can afford the purchase
        if value >= money[0]["cash"]:
            return apology("not enough money in account to purchase", 400)
        # insert the transaction into the history database with all info.
        db.execute("INSERT INTO history (id, transactionPrice, stockName, quantity, value, tickerSymbol, transactionType) VALUES (:id, :purchasePrice, :stockName, :quantity, :value, :tickerSymbol, :transactionType)",
                   id=session["user_id"], purchasePrice=usd(purchasePrice), stockName=quote["name"], quantity=shares, value=usd(value), tickerSymbol=quote["symbol"], transactionType="Buy")
        # check to see if the user already owns the stock
        rows = db.execute("SELECT * FROM portfolio WHERE id=:id AND stockName=:stockName",
                          id=session["user_id"], stockName=quote["name"])
        # if the user owns the stock
        if (rows):
            newQuantity = rows[0]["quantity"] + shares
            newValue = purchasePrice * newQuantity
            # update the portfolio with the number number of stocks
            db.execute("UPDATE portfolio SET quantity=:quantity WHERE id=:id AND tickerSymbol=:tickerSymbol",
                       quantity=newQuantity, id=session["user_id"], tickerSymbol=quote["symbol"])
            # update the portfolio for the new value
            db.execute("UPDATE portfolio SET value=:value WHERE id=:id AND tickerSymbol=:tickerSymbol",
                       value=usd(newValue), id=session["user_id"], tickerSymbol=quote["symbol"])
        # user didn't previously own the stock
        else:
            # insert a new row into the portfolio
            db.execute("INSERT INTO portfolio (id, stockName, tickerSymbol, currentPrice, quantity, value) VALUES (:id, :stockName, :tickerSymbol, :currentPrice, :quantity, :value)",
                       id=session["user_id"], stockName=quote["name"], tickerSymbol=quote["symbol"], currentPrice=usd(purchasePrice), quantity=shares, value=usd(value))
        # update the user's cash
        db.execute("UPDATE users SET cash=cash - :value WHERE id=:id", id=session["user_id"], value=value)
        # display the user's portfolio
        return redirect("/")
    else:
        return render_template("displayBuy.html")


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    username = request.args.get("username")
    # if the usernam is not already in the users database, return true
    if not (db.execute("SELECT * FROM users WHERE username=:username", username=username)):
        return jsonify(True)
    else:
        return jsonify(False)


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    # get all the user's previous transactions
    stocks = db.execute("SELECT * FROM history WHERE id=:id", id=session["user_id"])
    # display all the transactions
    return render_template("history.html", stocks=stocks)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username=:username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


# method for the user to deposit money
@app.route("/addMoney", methods=["GET", "POST"])
def addMoney():
    if request.method == "POST":
        # check to make sure the user inputed an int
        if not request.form.get("deposit").isdigit():
            return apology("Must enter int", 400)
        deposit = int(request.form.get("deposit"))
        cash = db.execute("SELECT cash FROM users WHERE id=:id", id=session["user_id"])
        # add the deposit to the previous cash
        balance = int(cash[0]["cash"]) + deposit
        # update the user's table for the new cash value
        db.execute("UPDATE users SET cash=:balance WHERE id=:id", id=session["user_id"], balance=balance)
        return redirect("/")
    else:
        return render_template("addMoney.html")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        quote = lookup(symbol)
        # make sure the user entered a valid symbol
        if not (quote):
            return apology("not a valid symbol", 400)
        quote["price"] = usd(quote["price"])
        return render_template("displayQuote.html", quote=quote)
    else:
        return render_template("searchQuote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # get the username the user entered
        username = request.form.get("username")
        # if the username is NULL, return an error
        if not username:
            return apology("must provide username", 400)
        # if the password is NULL, return an error
        if not (request.form.get("password")):
            return apology("must provide password", 400)
        # if the confirmation is NULL, return an error
        if not (request.form.get("confirmation")):
            return apology("must confirm your password", 400)
        # if the passwords don't match return an error
        if(request.form.get("password") != request.form.get("confirmation")):
            return apology("Your passwords do not match", 400)
        # hash the password
        hash = generate_password_hash(request.form.get("password"))
        # return an error if the username has been taken
        check = db.execute("SELECT * FROM users WHERE username=:username", username=username)
        if (check):
            return apology("Someone has already taken that username", 400)
        # insert the new user into the database
        db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)", username=username, hash=hash)
        user = db.execute("SELECT * FROM users WHERE username=:username", username=username)
        # put the user into the session
        session["user_id"] = user[0]["id"]
        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    if request.method == "POST":
        symbol = request.form.get("symbol")
        quote = lookup(symbol)
        # check to make sure the ticker symbol is a valid stock
        if not quote:
            return apology("not a valid symbol", 400)
        # check to make sure the user inputed an int
        if not request.form.get("shares").isdigit():
            return apology("Must enter int", 400)
        shares = int(request.form.get("shares"))
        # if the number of shares is not positive, return an error
        if not (shares > 0):
            return apology("you must input a non-negetive number", 400)
        # obtain the number of shares of the stock the user owns
        share = db.execute("SELECT * FROM portfolio WHERE id=:id AND tickerSymbol=:tickerSymbol",
                           id=session["user_id"], tickerSymbol=quote["symbol"])
        # if the user does not own the stock, return an error
        if not share:
            return apology("You do not own that stock", 400)
        oldShares = share[0]["quantity"]
        # ensure the user has enough shares to sell the amount they entered
        if (shares > oldShares):
            return apology("You cannot sell more shares than you have", 400)
        salePrice = quote["price"]
        value = salePrice * shares
        # update the new amount of cash after the sale
        db.execute("UPDATE users SET cash=cash + :newCash WHERE id=:id", id=session["user_id"], newCash=value)
        # insert the transaction in the the history database
        db.execute("INSERT INTO history (id, transactionPrice, stockName, quantity, value, tickerSymbol, transactionType) VALUES (:id, :salePrice, :stockName, :quantity, :value, :tickerSymbol, :transactionType)",
                   id=session["user_id"], salePrice=usd(salePrice), stockName=quote["name"], quantity=shares, value=usd(value), tickerSymbol=quote["symbol"], transactionType="Sell")
        # if selling all their shares of the stock
        if (shares is oldShares):
            # remove the whole row from the portfolio
            db.execute("REMOVE FROM portfolio * WHERE id=:id AND tickerSymbol=:tickerSymbol",
                       id=session["user_id"], tickerSymbol=quote["symbol"])
        else:
            newShares = oldShares - shares
            newValue = newShares * salePrice
            # update the portfolio.  Subtract the number of shares sold.
            db.execute("UPDATE portfolio SET quantity=:shares WHERE id=:id AND tickerSymbol=:tickerSymbol",
                       shares=newShares, id=session["user_id"], tickerSymbol=quote["symbol"])
            # update the portfolio.  Subtract the value of the sale
            db.execute("UPDATE portfolio SET value=:newValue WHERE id=:id AND tickerSymbol=:tickerSymbol",
                       newValue=usd(newValue), id=session["user_id"], tickerSymbol=quote["symbol"])
        return redirect("/")
    else:
        # get the list of stocks the user owns
        stocks = db.execute("SELECT tickerSymbol FROM portfolio WHERE id=:id", id=session["user_id"])
        if not stocks:
            return apology("You do not own any stocks", 400)
        return render_template("displaySell.html", stocks=stocks)


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
