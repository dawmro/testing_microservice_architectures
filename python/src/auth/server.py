import jwt, datetime, os
from flask import Flask, request
from flask_mysqldb import MySQL


# create server as a Flask object
server = Flask(__name__)

# config for mysql connection
server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
server.config["MYSQL_PORT"] = os.environ.get("MYSQL_PORT")

# connect Flask to MySQL database
mysql = MySQL(server)




# create login route
@server.route("/login", methods =["POST"])
def login():
    # get user data from basic authentication scheme
    auth = request.authorization
    if not auth:
        return "missing credentials", 401
    
    # check database for login and password where email matches username that came in a request   
    cur = mysql.connection.cursor()
    res = cur.execute( 
        "SELECT email, password FROM user WHERE email=%s, (auth.username,)
    )
    
    # if user exists in database
    if res > 0:
        user_row = cur.fetchone()
        email = user_row[0]
        password = user_row[1]
        
        # check if username and password match the ones from request 
        if auth.username != email or auth.password != password:
            return "invalid credentials", 401
        else:
            # return JWT using username and secret from virtual env
            # todo
            #return createJWT(auth.username, os.environ.get("JWT_SECRET"), True)
    # if such user does not exists, then credentials are invalid
    else:
        return "invalid credentials", 401
