from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp

from helpers import *

# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# custom filter
app.jinja_env.filters["usd"] = usd

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@app.route("/")
@login_required
def index():
    """Show the current holdings"""
    
    if request.method == "POST":
        return index()
    
    elif request.method == "GET":
        
        # make a list of dictionaries of all the current holdings 
        port_dict = db.execute("SELECT * FROM 'portfolios' WHERE user_id = :user_id", user_id=session["user_id"])
        lenportfolio = len(port_dict)

        # lookup the value of all the stocks in the portfolio, and return them in a list 
        lookups = []
        for i in range(lenportfolio):
            symbol = port_dict[i]['symbol']
            info  = lookup(symbol)
            value = info['price']
            lookups.append(value)
        
        # calculate the total value of the portfolio
        total_value = 0
        for i in range(lenportfolio):
            total_value += lookups[i] * port_dict[i]['number']

        # lookup the total amount of cash
        cash = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])[0]['cash']

        # return the index
        return render_template("index.html", port_dict=port_dict, lenportfolio=lenportfolio, lookups=lookups, total_value=total_value, cash=cash)
    

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock."""
    
    # if the user used the 'buy button' on the index page, return the pre-loaded pages
    if request.form.get("symbol_to_buy"):
        return render_template("buy_pre.html", symbol=request.form.get("symbol_to_buy"))
    
    elif request.method == "GET":
        return render_template("buy.html")

    elif request.method == "POST":
        
        # user must provide a symbol
        if not request.form.get("symbol"):
            return apology("must provide symbol")
            
        # user must provide an existing symbol
        elif not lookup(request.form.get("symbol")):
            return apology("can't find the symbol")
            
        # user must provide a positive integer
        try:
            shares=int(request.form.get("shares"))
        except ValueError:
            return apology("number of shares is not a positive integer")
        if shares <= 0:
            return apology("number of shares is not a positive integer")
        
        # creates variables for (total)price, symbol, current cash and user_id
        info = lookup(request.form.get("symbol"))
        price = info['price']
        total_price = price * shares
        symbol = info['symbol']
        cash = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])[0]['cash']
        user_id = session["user_id"]
        
        # if the user hasn't enough cash, return an apolgy
        if int(cash) < total_price:
            return apology("not enough cash to complete this transaction")
            
        # else, insert the transaction in the transaction table, update the users amount of cash and update his/her portfolio
        else:
            db.execute("INSERT INTO 'transactions' (name_id, symbol, number, price) VALUES (:user_id, :symbol, :shares, :price)", user_id=user_id, symbol=symbol, shares=shares, price=price)
            db.execute("UPDATE 'users' SET cash = cash - :total_price WHERE id = :user_id", total_price=total_price, user_id=user_id)
            
            # if the user already has one, or more shares of this stock, add the new stock to it's current stock in his portfolio, otherwise make a new line
            rows = db.execute("SELECT * FROM 'portfolios' WHERE user_id = :user_id AND symbol = :symbol", user_id=user_id, symbol=symbol)
            if len(rows) > 0:
                db.execute("UPDATE 'portfolios' SET number = (number + :number) where user_id = :user_id AND symbol = :symbol", number=shares, user_id=user_id, symbol=symbol)
            else:
                db.execute("INSERT INTO 'portfolios' (user_id, symbol, number) VALUES (:user_id, :symbol, :number)", user_id=user_id, symbol=symbol, number=shares)

        # return the index
        return redirect(url_for("index"))


@app.route("/history")
@login_required
def history():
    """Show history of transactions."""
    
    if request.method == "POST":
        return history()
    
    elif request.method == "GET":
        
        # makes a list of dictionaries of all the transactions 
        trans_dict = db.execute("SELECT * FROM 'transactions' WHERE name_id = :user_id", user_id=session["user_id"])
        lentransactions = len(trans_dict)
        
        # makes a list of every transaction with if it was bought or sold 
        bought_sold = []
        for i in range(len(trans_dict)):
            if trans_dict[i]['number'] > 0:
                bought_sold.append('Bought')
            else:
                bought_sold.append('Sold')

        # return the history template
        return render_template("history.html", trans_dict=trans_dict, lentransactions=lentransactions, b_s=bought_sold)
    

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return apology("invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")

    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("must provide symbol")
        elif not lookup(request.form.get("symbol")):
            return apology("can't find the symbol")
        else:
            info = lookup(request.form.get("symbol"))
            name = info['name']
            price = info['price']
            symbol = info['symbol']
            return render_template("quoted.html", name=name, price=price, symbol=symbol)

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""
    
    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # ensure password confirmation was submitted
        elif not request.form.get("password_again"):
            return apology("must provide password twice")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))
        
        # ensure username does not already exists
        if len(rows) != 0:
            return apology("username already exists")
        elif request.form.get("password") != request.form.get("password_again"):
            return apology("passwords do not match")

        # add user information to database
        else:
            db.execute("INSERT INTO users (username, hash) VALUES (:username,:hash)", username=request.form.get("username"), hash=pwd_context.hash(request.form.get("password")))

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")
    

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock."""
    
    # if the user used the 'sell button' on the index page, return the pre-loaded pages
    if request.form.get("symbol_to_sell"):
        return render_template("sell_pre.html", symbol=request.form.get("symbol_to_sell"))

    elif request.method == "GET":
        return render_template("sell.html")

    elif request.method == "POST":
        # user must provide a symbol
        if not request.form.get("symbol"):
            return apology("must provide symbol")
        
        # user must provide a valid symbol
        elif not lookup(request.form.get("symbol")):
            return apology("can't find the symbol")
        
        # user must provide a positive integer
        try:
            shares=int(request.form.get("shares"))
        except ValueError:
            return apology("number of shares is not a positive integer")
        if shares <= 0:
            return apology("number of shares is not a positive integer")
        
        # initiate multiple variables
        info = lookup(request.form.get("symbol"))
        price = info['price']
        shares = -shares
        total_price = price * shares
        symbol = info['symbol']
        user_id = session["user_id"]

        # check if the user has anough shares in his/her portfolio
        shares_owned_dict = db.execute("SELECT number FROM portfolios WHERE user_id = :user_id AND symbol LIKE :symbol", user_id=user_id, symbol=symbol)
        shares_owned = int(shares_owned_dict[0]['number'])
        if -shares > shares_owned:
            return apology("not enough shares to complete this transaction")

        # else, insert the transaction in the transaction table, update the users amount of cash and update his/her portfolio
        db.execute("INSERT INTO 'transactions' (name_id, symbol, number, price) VALUES (:user_id, :symbol, :shares, :price)", user_id=user_id, symbol=symbol, shares=shares, price=price)
        db.execute("UPDATE 'users' SET cash = cash - :total_price WHERE id = :user_id", total_price=total_price, user_id=user_id)

        # if the user has sold all his/her shars, remove the stock from the portfolio, otherwise update the stock in the portfolio
        if shares_owned + shares == 0:
            db.execute("DELETE FROM 'portfolios' WHERE user_id = :user_id AND symbol = :symbol", user_id=user_id, symbol=symbol)
        else:
            db.execute("UPDATE 'portfolios' SET number = (number + :number) where user_id = :user_id AND symbol = :symbol", number=shares, user_id=user_id, symbol=symbol)
        
        # redirect to the index page
        return redirect(url_for("index"))



@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    """Change account information."""
    
    if request.method == "GET":
        return render_template("account.html")

    if request.method == "POST":
        # user must provide the current password
        if not request.form.get("old_password"):
            return apology("must provide old password")
            
        # user must provide the new password
        elif not lookup(request.form.get("new_password")):
            return apology("must provide new password")
            
        # user must provide the confirmation of the new password
        elif not lookup(request.form.get("new_password_again")):
            return apology("must confirm new password")
            
        else:
            # make variables for the old and new passwords
            stored_password = db.execute("SELECT hash FROM users WHERE id = :id", id=session["user_id"])
            old_password = request.form.get("old_password")
            new1_password = request.form.get("new_password")
            new2_password = request.form.get("new_password_again")
            
            # check if the given current password is the same as the current password
            if not pwd_context.verify(old_password, stored_password[0]["hash"]):
                return apology("Current password not correct")
            
            # check if the new password is the same as the confirmation of the new password
            elif new1_password != new2_password:
                return apology("New passwords don't match")
            
            # update password
            else:
                db.execute("UPDATE 'users' SET hash = :newhash where id = :id", newhash=pwd_context.hash(new1_password), id=session["user_id"])
                
                # return to the index page
                return redirect(url_for("index"))
                
                
@app.route("/transfer", methods=["GET", "POST"])
@login_required
def transfer():
    """Transfer money."""
    
    if request.method == "GET":
        return render_template("transfer.html")

    if request.method == "POST":
        # make a variable called amount
        amount = 0
        
        # check if the user wants to insert money
        if request.form.get("insert") and not request.form.get("withdraw"):
            
            # check if the entered amount is a positive integer
            try:
                amount=int(request.form.get("insert"))
            except ValueError:
                return apology("number of shares is not a positive integer")
            if amount <= 0:
                return apology("number of shares is not a positive integer")
          
        # check if the user wants to withdraw money      
        elif request.form.get("withdraw"):
            
            # check if the entered amount is a positive integer
            try:
                amount=-int(request.form.get("withdraw"))
            except ValueError:
                return apology("number of shares is not a positive integer")
            if amount >= 0:
                return apology("number of shares is not a positive integer")
            
            # check if the user has enough cash to complete the transaction
            cash = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])
            if -amount > cash[0]['cash']:
                return apology("not enough cash to complete this transaction")
        
        # user must provide an amount      
        else:
            return apology("Must provide amount")

        # update the cash balance of the user
        db.execute("UPDATE 'users' SET cash = cash + :amount WHERE id = :user_id", amount=amount, user_id=session["user_id"])
        
        # return the index page
        return redirect(url_for("index"))